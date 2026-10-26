#!/usr/bin/env python3
"""Nutstore WebDAV client. Fixed HTTPS origin, create-only writes, private credentials."""
import argparse
import base64
import getpass
import http.client
import json
import os
from pathlib import Path
import ssl
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit
import xml.etree.ElementTree as ET

HOST = 'dav.jianguoyun.com'
LIMIT = 512 * 1024 * 1024
CONFIG = Path.home() / '.config' / 'zeroclaw-apps' / 'nutstore' / 'credentials.json'


def remote_path(value):
    if not value.startswith('/') or '\\' in value or any(ord(c) < 32 for c in value):
        raise ValueError('invalid_path')
    parts = value.split('/')
    if any(part in ('.', '..') for part in parts):
        raise ValueError('invalid_path')
    return '/dav/' + '/'.join(quote(p, safe='') for p in parts if p)


def write_path(value):
    remote_path(value)
    if value.rstrip('/') != '/ZeroClaw' and not value.startswith('/ZeroClaw/'):
        raise ValueError('write_outside_zeroclaw')


def credentials(path=CONFIG):
    if path.is_symlink() or not path.is_file():
        raise ValueError('configure_required')
    if os.name == 'posix' and path.stat().st_mode & 0o077:
        raise ValueError('credentials_permissions')
    value = json.loads(path.read_text())
    if not value.get('account') or not value.get('password'):
        raise ValueError('configure_required')
    return value


def configure(path=CONFIG):
    account = input('Nutstore account: ').strip()
    password = getpass.getpass('Dedicated application password: ')
    if not account or not password or ':' in account:
        raise ValueError('invalid_credentials')
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.parent.is_symlink() or path.is_symlink():
        raise ValueError('unsafe_config_path')
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent, delete=False) as output:
        temporary = Path(output.name)
        try:
            os.chmod(temporary, 0o600)
            json.dump({'account': account, 'password': password}, output)
            output.flush()
            os.fsync(output.fileno())
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    return {'configured': True}


def request(method, path, body=None, headers=None):
    auth = credentials()
    token = base64.b64encode((auth['account'] + ':' + auth['password']).encode()).decode()
    merged = {'Authorization': 'Basic ' + token, 'User-Agent': 'ZeroClaw-Nutstore/1.0'}
    merged.update(headers or {})
    conn = http.client.HTTPSConnection(HOST, timeout=45, context=ssl.create_default_context())
    try:
        conn.request(method, remote_path(path), body=body, headers=merged)
        response = conn.getresponse()
        # Never follow redirects with credentials, even to the same host.
        if response.status not in (200, 201, 204, 207):
            if response.status in (401, 403):
                raise ValueError('authorization_failed')
            if response.status == 412:
                raise ValueError('destination_exists')
            raise ValueError('http_' + str(response.status))
        return conn, response
    except BaseException:
        conn.close()
        raise


def list_files(path):
    body = b'<?xml version="1.0"?><d:propfind xmlns:d="DAV:"><d:prop><d:displayname/><d:getcontentlength/><d:resourcetype/></d:prop></d:propfind>'
    conn, response = request('PROPFIND', path, body, {'Depth': '1', 'Content-Type': 'application/xml'})
    try:
        raw = response.read(2 * 1024 * 1024 + 1)
    finally:
        conn.close()
    if len(raw) > 2 * 1024 * 1024 or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('invalid_response')
    root = ET.fromstring(raw)
    result = []
    target = unquote(remote_path(path)).rstrip('/')
    for item in root.findall('{DAV:}response'):
        href = item.findtext('{DAV:}href', '')
        url = urlsplit(href)
        if url.netloc and (url.scheme != 'https' or url.netloc != HOST):
            continue
        decoded = unquote(url.path).rstrip('/')
        if decoded == target or not decoded.startswith(target + '/'):
            continue
        relative = decoded[len(target) + 1:]
        if '/' in relative or relative in ('.', '..'):
            continue
        prop = item.find('{DAV:}propstat/{DAV:}prop')
        if prop is None:
            continue
        result.append({'name': relative, 'path': decoded[4:],
                       'directory': prop.find('{DAV:}resourcetype/{DAV:}collection') is not None,
                       'bytes': prop.findtext('{DAV:}getcontentlength')})
    return {'entries': result, 'count': len(result), 'recursive': False}


def download(path, local):
    target = Path(local)
    if not target.is_absolute() or target.exists() or target.is_symlink():
        raise ValueError('local_destination_conflict')
    conn, response = request('GET', path)
    temporary = None
    size = 0
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as output:
            temporary = Path(output.name)
            while True:
                block = response.read(65536)
                if not block:
                    break
                size += len(block)
                if size > LIMIT:
                    raise ValueError('download_too_large')
                output.write(block)
            output.flush()
            os.fsync(output.fileno())
        if response.getheader('Content-Length') and size != int(response.getheader('Content-Length')):
            raise ValueError('incomplete_download')
        os.link(temporary, target)  # Exclusive publication; never overwrite a racing file.
    finally:
        conn.close()
        if temporary:
            temporary.unlink(missing_ok=True)
    return {'path': str(target), 'bytes': size}


def mutate(action, path, local, confirmed):
    write_path(path)
    if not confirmed:
        raise ValueError('confirmation_required')
    if action == 'mkdir':
        conn, response = request('MKCOL', path)
    else:
        source = Path(local)
        if not source.is_absolute() or source.is_symlink() or not source.is_file() or source.stat().st_size > LIMIT:
            raise ValueError('invalid_local_source')
        with source.open('rb') as stream:
            conn, response = request('PUT', path, stream,
                                     {'Content-Length': str(os.fstat(stream.fileno()).st_size),
                                      'If-None-Match': '*', 'Content-Type': 'application/octet-stream'})
    conn.close()
    return {'path': path, 'action': action, 'httpStatus': response.status}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['capabilities', 'configure', 'disconnect', 'list', 'download', 'upload', 'mkdir'])
    parser.add_argument('--path', default='/')
    parser.add_argument('--local')
    parser.add_argument('--confirm', action='store_true')
    args = parser.parse_args()
    if args.action == 'capabilities':
        return {'commands': ['configure', 'disconnect', 'list', 'download', 'upload', 'mkdir'],
                'endpoint': 'https://' + HOST + '/dav/', 'writeRoot': '/ZeroClaw', 'overwrite': False}
    if args.action == 'configure':
        return configure()
    if args.action == 'disconnect':
        if not args.confirm:
            raise ValueError('confirmation_required')
        CONFIG.unlink(missing_ok=True)
        return {'disconnected': True}
    if args.action == 'list':
        return list_files(args.path)
    if args.action == 'download':
        return download(args.path, args.local or '')
    return mutate(args.action, args.path, args.local or '', args.confirm)


if __name__ == '__main__':
    try:
        print(json.dumps({'status': 'SUCCESS', 'data': main()}, ensure_ascii=False))
    except (ValueError, OSError, http.client.HTTPException, ET.ParseError) as error:
        # Never print credential-bearing exceptions, headers or response bodies.
        code = str(error) if isinstance(error, ValueError) and str(error).replace('_', '').isalnum() else 'request_failed'
        print(json.dumps({'status': 'FAILED', 'error': code}))
        sys.exit(1)
