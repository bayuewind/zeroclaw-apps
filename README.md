# ZeroClaw Apps

A curated application catalog for ZeroClaw.

## Status

The catalog lists CC Switch CLI, Magpie CLI, Codex desktop, Clash Verge Rev, China Mobile Cloud and Nutstore. Compatible
ZeroClaw clients load this feed and retain a pinned offline snapshot. Publishing
a listing does not make it installable in a client without its matching adapter.

## Catalog

[`registry.json`](registry.json) is the source of truth for curated listings and
presentation order. The public feed is:

<https://raw.githubusercontent.com/bayuewind/zeroclaw-apps/main/registry.json>

The document has `schema_version: 1` and an `apps` array. Each entry contains:

| Field | Meaning |
| --- | --- |
| `id` | Stable application identity matching a supported ZeroClaw installer adapter |
| `name` | Display name |
| `repository` | Official source repository link for display |
| `author` | Upstream project owner |
| `summary` | Plain text description by language (`en` and `zh`) |
| `keywords` | Search terms |

Array order is discovery order. Each application id must be unique. Keep the
English and Chinese summaries together when changing a listing.

## Curation

Propose changes through pull requests. Maintainers review the official source,
application purpose and client support before merging a listing. Changes to
selection, ordering and descriptions can be delivered without repackaging Zero
once a compatible client integrates this feed.

Do not add latest-version values, download commands, arbitrary install scripts,
local paths, credentials, installed state or permission settings to this catalog.
Official release feeds own versions and artifacts. Zero owns supported install
adapters and permissions. Local disk observations and matching receipts determine
installed state and whether Zero may update or remove an application.

A new application or installation method requires corresponding client support.
Removing a discovery listing must not uninstall an application or hide it from
the client's installed view. Catalog revisions are Git commits; revert a change
to publish a rollback. Clients should retain their last valid catalog when a
refresh fails.

## 中文说明

这里维护 ZeroClaw 精选应用的介绍、顺序和搜索关键词，包含 CC Switch CLI、
Magpie CLI、Codex 桌面版、Clash Verge Rev、中国移动云盘和坚果云。兼容的 Zero 客户端读取远程清单并保留固定版本的离线快照。

后续通过 PR 提交精选应用变更。安装包、版本和校验信息继续来自官方发布源；
安装、更新、卸载以及配置权限由 Zero 管理。新增应用仍需要客户端提供相应支持。


## Cloud applications

Cloud listings install local agent capability packages and link to their web
applications. They do not wrap a browser session or install a desktop client.
The client pins package sources and SHA-256 values independently of this catalog.
Updates require a reviewed client pin; mutable upstream changes fail closed.

- China Mobile Cloud: upstream SkillHub package
  `@org-vt43r0t0/cm-cloud-manage`, release 2.0.2. See
  [source pin](packages/cm-cloud-manage.json). The upstream package is downloaded
  directly, never republished here. Its scripts require Python 3.10+; installation
  does not install dependencies or authorize the user's account.
- Nutstore: [maintained WebDAV skill](packages/nutstore/SKILL.md) using the
  [official service](https://help.jianguoyun.com/?tag=webdav). Run
  `python3 packages/build.py` to rebuild its deterministic archive. This is a
  ZeroClaw integration, not an official Nutstore client. Configure a dedicated
  application password locally; read access covers the account, writes are
  create-only and limited to `/ZeroClaw`. Credentials are stored in a mode-0600
  local file outside the installed skill, without encryption; protect the OS
  account and revoke the dedicated password in Nutstore when no longer needed.

Zero installs these skills beneath its existing shared skill directory. Users
choose a skill bundle and agent through existing configuration; package install
never enables script execution or grants an agent additional tool permissions.
Uninstall preserves remote files and local credentials. Disconnect/revoke an
account separately. Backups are retained for manual recovery. Skills and scripts
remain subject to the client's existing audit and tool permission checks.
