# ZeroClaw Apps

A curated application catalog for ZeroClaw.

## Status

The catalog lists CC Switch CLI, Magpie CLI and Codex desktop. Compatible
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
Magpie CLI 和 Codex 桌面版。兼容的 Zero 客户端读取远程清单并保留固定版本的离线快照。

后续通过 PR 提交精选应用变更。安装包、版本和校验信息继续来自官方发布源；
安装、更新、卸载以及配置权限由 Zero 管理。新增应用仍需要客户端提供相应支持。
