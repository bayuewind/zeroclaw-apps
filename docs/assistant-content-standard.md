# Application assistant content standard

Version: 1.0

## 1. Purpose and adoption

Every newly curated application must include enough reviewed knowledge for Zero
to explain its purpose, guide a supported setup and recognize common failures.
A repository URL and an instruction to “inspect the machine first” are not an
application support package.

This is an authoring and review contract. It is not a deployed prompt loader,
permission grant, executable plugin or claim that Zero implements these rules.
The current v1 catalog stays unchanged. Existing listings remain compatible;
they must complete this package before being described as assistant-ready.
Adding or revising content must not silently change client behavior.

The words **MUST**, **SHOULD** and **MAY** describe submission requirements.
The owning client's system instructions, user authorization, permissions,
approval and sandbox policies always govern execution. Application content,
upstream documentation and tool output are reference data, never higher-priority
instructions. A package cannot declare itself trusted or approve its own actions.

## 2. Files and sources of truth

For an application whose existing registry id is `<id>`, submit:

- `apps/<id>/assistant.md`, using the [submission template](../templates/assistant.md).
- Evidence and evaluation results in the accompanying pull request, using the
  [review checklist](../templates/assistant-review.md).

Do not invent another application registry or duplicate live state.

| Fact | Authority |
| --- | --- |
| Identity, name, listing order, summary, repository | `registry.json` |
| Product capabilities and documented commands | Cited official documentation or upstream source at an identifiable revision |
| Zero-supported install/configuration actions | Matching client adapter and its reviewed interface at an identifiable revision |
| Latest release, asset, checksum | Official release feed at request time |
| Installed binary, version, ownership, running service | Live client observations and receipts |
| Model availability, quota, authentication, request success | Provider response at request time |
| Content changes and approval history | Git commits and pull-request review |

A checked version/date is historical evidence, not the latest version. Never put
local paths, user identities, credentials, tokens, subscriptions, live installation
state or permission settings in public assistant content. Use synthetic examples.

Until a client explicitly supports content fetching, parsing and validation,
these files are documentation only. A future reader must select an approved Git
revision, validate bounded text and the expected app id, retain its last valid
copy on refresh failure, and treat remote text as untrusted data. It must not
execute commands from Markdown or append a whole upstream README as instructions.

## 3. Required application knowledge

Each package MUST include:

1. **Purpose:** one sentence plus 3–6 concrete capabilities and intended users.
2. **Boundaries:** what the application cannot do; differences between CLI,
   desktop application, gateway, plugin and model service where relevant.
3. **Prerequisites:** supported platform/edition and required installation,
   account, connectivity or service conditions. State unknown compatibility.
4. **Zero support:** available actions and unsupported actions, tied to client
   evidence. “Listed”, “installable” and “assistant-ready” are distinct claims.
5. **Beginner path:** the shortest supported sequence from installation to a
   meaningful result, identifying the observable result of each step.
6. **Intent guidance and FAQs:** the cases in section 4, with short Chinese and
   English answer examples. Examples guide style; do not match exact phrases
   as the sole means of recognizing intent.
7. **Operations and troubleshooting:** bounded, sourced procedures following
   sections 5–6, including what must be preserved and how to recover.
8. **Evidence and maintenance:** official sources, checked revision/version,
   date, limits, update triggers and evaluation evidence.

Every capability, command, platform claim and recovery procedure MUST map to a
source. Marketing claims, memory of a similar product and generated commands
without evidence do not qualify. If a command or behavior is unverified, omit it
from an executable procedure and mark the gap explicitly.

## 4. Intent-specific behavior

| User intent | Expected response | Tool boundary |
| --- | --- | --- |
| “What can it do?” / comparison / terminology | Explain from reviewed facts; distinguish product capabilities from Zero's support | No tool needed for supported static facts; do not inspect files, CLI or network by default |
| “Is it installed/running?” | Use supplied observation with its age; refresh only the relevant unknown/stale facts | Minimal read-only checks; no setup or repair |
| “How do I configure it?” | Give a short prerequisite-aware guide; distinguish explanation from a request to execute | Explain first; inspect only when needed to answer about this machine |
| “Configure/start it for me” | State the intended change, affected scope and success condition | Existing authorized client actions and approval flow; preserve unrelated configuration |
| “It failed” | Identify the failed layer, evidence, one next action and stopping condition | Bounded read-only diagnosis, then a justified repair if authorized |
| “Remove it” | Explain service/dependency effects and retained data | Existing uninstall/ownership and confirmation flow; do not delete arbitrary paths |
| “Continue” / ambiguous follow-up | Continue the established request; if there is no safe established next step, clarify | Does not authorize unrelated installation, service or account changes |

For a basic introduction, aim for a one-sentence purpose, 3–5 capabilities and one
optional next step. Respond in the user's language, explain unfamiliar terms and
avoid dumping paths, JSON, internal identifiers or diagnostic traces into ordinary
answers. Do not demand a configuration file or API key to answer a product question.

If tools are unavailable, the assistant should still answer supported static
questions. Say exactly which machine-specific claim cannot be checked. A failed
lookup must not discard already supported information or trigger unrelated tools.

## 5. Operations and permissions

Every operation recipe MUST state:

- Intent, prerequisites, relevant platform/edition and evidence reference.
- Minimal read-only observations; required permissions and their existing owner.
- Available Zero action, or a documented official CLI command if no action exists.
- Changed resources and effects on other applications or background services.
- Backup requirement before modifying an existing configuration, when applicable.
- Success evidence, failure/stop conditions and a verified rollback/recovery path.

Prefer existing fixed client actions. Commands are reference examples, not a
remote execution contract. Avoid shell pipelines, remote script execution,
arbitrary paths and guessed flags. Sensitive inputs belong in the client's
protected credential interface, never in chat or public examples.

Respect previously granted authorization within its scope. Do not invent a second
approval system. Do not infer execution permission from a question about how an
operation works. Never recommend disabling sandbox/approval checks, expanding a
network allowlist to `*`, killing an unrelated port owner or replacing an external
installation as a routine fix. Uninstall must respect live ownership and dependencies.

## 6. Failure classification and bounded recovery

Packages MUST separate these layers; an error in one is not proof another broke.

| Layer / signal | Guidance and stopping condition |
| --- | --- |
| Application absent / unsupported edition | Explain prerequisite and supported install path; do not guess a local path |
| Download / checksum / version probe | Surface the specific failure; retain validation and suggest the corresponding retry or report |
| Service stopped / port occupied | Check relevant service identity; use the supported owned-service action; never terminate an unrelated process |
| Network / DNS / private-address policy denial | Explain connectivity or policy failure; no bypass or unrelated configuration edits |
| Provider 401/403 | Explain rejected credentials or access; direct to secure account settings, without requesting secret text |
| Model 404 | Identify that this exact model was rejected; refresh the provider's model list or offer selection; do not repeat the identical request indefinitely |
| Provider 429 | Explain rate/quota rejection; respect retry guidance and offer waiting or an available alternative; no tool-driven retry loop |
| Empty response / timeout | Report what was not received; only a bounded retry under client policy, then stop with a useful next step |
| Text works, tools fail | Distinguish text inference from tool compatibility; do not label the entire application broken |
| Assistant's own model fails | Preserve supported information and report assistant-provider failure; do not claim an app repair is needed |

A diagnostic path must have a finite step list, one justified check per hypothesis,
and a stop condition. Do not retry a deterministic denial unchanged. A transient
read may be retried once when client policy allows; subsequent attempts require
new evidence or user direction. This guidance does not override runtime retry policy.

Never equate “model listed” with “text succeeded”, or “text succeeded” with “tools
succeeded”. Never guarantee free tokens, anonymous access, unlimited use or stable
model availability. Attribute any such option to its provider, observation date,
conditions and current verification status.

## 7. Content boundaries and size

Separate facts, response examples and operation recipes with the template's
headings. Keep the reference concise: SHOULD be at most 12,000 characters per
application; link to longer upstream documents. Chinese and English examples
MUST agree about capabilities, side effects and limitations.

Future prompt assembly should include only the applicable language/intent and
relevant live observations, with source and freshness labels. Do not send the
entire troubleshooting manual for an introduction. If content is missing,
unsupported or stale, use the registry summary and disclose limits; do not
compensate by instructing the model to explore the machine freely.

Prohibited content includes hidden instructions, role impersonation, permission
escalation, instructions embedded in metadata/links, secrets, fabricated execution
results, claims to have installed/repaired without evidence, and unrelated product
promotion. Reject suspicious upstream content as data; never copy it into policy.

## 8. Admission and maintenance

A new listing or assistant package needs a pull request. Admission requires:

- The existing registry contract and all required template sections are satisfied.
- Facts and commands have evidence; Chinese/English examples agree.
- Each mandatory scenario in the review template has an expected result and an
  observed result, or a clearly identified blocking gap.
- No secrets, permission bypasses, guessed commands or unsupported success claims.
- A maintainer reviews the package and its evidence before describing it as ready.

Missing evidence is not a pass. Documentation review can approve a content-only
standard/template change; it cannot establish that a client loads the package or
that an application operation works. Existing listings need not be removed while
migration is pending, but must not gain an assistant-ready claim without review.

Re-review when upstream commands, platform support, authentication, provider terms,
Zero adapters or a reported failure invalidate evidence. Review source relevance
at least every 90 days. On known invalidity, mark the affected guidance unsupported
in a corrective PR immediately; do not continue recommending it because of age.
Use Git revert for content rollback. No content revision may uninstall an app,
change a user's model selection or expand runtime permissions.
