# Example: a Magpie introduction

This illustrates the standard's answer shape. It is not a complete, approved
Magpie package or evidence of model/tool evaluation. Product facts below come
only from the existing `registry.json` Magpie summary at commit `44d9d06`.
A full package still needs upstream capability and command evidence.

## User question

“Magpie 能做什么？” / “What can Magpie do?”

## Facts available

- The listed edition is Magpie CLI.
- It brings model services and plugins together in a local gateway.
- Zero and other AI tools can use that gateway for model access.
- No supplied observation proves a running gateway, quota or successful inference.

## Example Chinese answer

Magpie 可以把模型服务和插件汇集到一个本地网关，让 Zero 和其他 AI 工具通过它接入模型。

你可以把它理解为模型服务的统一入口。我们收录的是 Magpie CLI。
它能否使用某个模型、有没有免费额度，要看模型来源以及当时的实际调用结果。

如果你想让 Zero 使用它，下一步可以了解应用卡片里的模型接入流程。

## Example English answer

Magpie brings model services and plugins together in a local gateway that Zero
and other AI tools can use to access models. Think of it as a common entry point
for model services. This listing is for Magpie CLI.

Whether a particular model works or has free allowance depends on its provider
and current request results. If you want Zero to use it, the next step is to
review the model connection flow in the app card.

## Why this fits

The answer uses available product facts and does not require a shell command,
README download, account credential or service start. It neither promises free
access nor claims that the gateway is running. Execution requires a separate,
scoped user request and the client's existing authorization mechanisms.
