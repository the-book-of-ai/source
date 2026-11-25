<!-- Generated from ai-tools.csv. Do not edit by hand. -->

## Inference engines and runners

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | Inference engine | MIT | CLI, Self-hosted | GGUF inference on CPU and GPU, pushed 25 Nov 2026 | You bring the weights and the server flags | In chapter 3 |
| [Ollama](https://github.com/ollama/ollama) | Model runner | MIT | Desktop, CLI | Installers for macOS, Windows, and Linux; local library plus an API | README also mentions cloud access; this row is the local app | [Omarchy manual](https://github.com/omacom/omarchy/blob/quattro/manual/17-ai.md) recommends it. Chapter 3 and glossary PR 27 |
| [vLLM](https://github.com/vllm-project/vllm) | Inference engine | Apache-2.0 | CLI, Self-hosted | High-throughput OpenAI-compatible serving, pushed 25 Nov 2026 | Built for serving many requests, not a desktop chat app | Chapter 3 and glossary PR 27 |
| [SGLang](https://github.com/sgl-project/sglang) | Inference engine | Apache-2.0 | CLI, Self-hosted | Serving framework for language and multimodal models, pushed 25 Nov 2026 | A server you operate, not a packaged desktop app | Chapter 3 and glossary PR 27 |
| [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) | Inference engine | Apache-2.0 | Self-hosted | NVIDIA's LLM serving stack; LICENSE text is Apache-2.0 | GitHub's license detector does not emit an SPDX id | Chapter 3 |
| [Transformers](https://github.com/huggingface/transformers) | Inference library | Apache-2.0 | Self-hosted | Reference library for running Hub models, pushed 25 Nov 2026 | Python runtime; slower than a dedicated server | Chapter 3 |
| [mlx-lm](https://github.com/ml-explore/mlx-lm) | Inference engine | MIT | Self-hosted | Runs LLMs on Apple's MLX array framework | Apple silicon path; not a Windows or NVIDIA runner | Chapter 3 |
| [OpenVINO](https://github.com/openvinotoolkit/openvino) | Inference engine | Apache-2.0 | Self-hosted | Intel toolkit for CPU, GPU, and NPU inference | Tied to Intel's runtime | Chapter 3 |
| [ExLlamaV3](https://github.com/turboderp-org/exllamav3) | Inference engine | MIT | Self-hosted | Quantized local inference on consumer NVIDIA GPUs | NVIDIA-only by the repo description | Chapter 3 |
| [ik_llama.cpp](https://github.com/ikawrakow/ik_llama.cpp) | Inference engine | MIT | CLI, Self-hosted | llama.cpp fork with extra quants, pushed 25 Nov 2026 | A fork: behavior can diverge from upstream llama.cpp | Chapter 3 and glossary PR 27 |
| [KTransformers](https://github.com/kvcache-ai/ktransformers) | Inference engine | Apache-2.0 | Self-hosted | Heterogeneous CPU/GPU inference and fine-tune optimizations | Niche offload stack, not a general model library | Chapter 3 PR 26 |
| [Strata](https://github.com/Niko1221/Strata) | Inference engine | MIT | Desktop, Self-hosted | One-click Windows and Linux install; local OpenAI/Anthropic API | Description limits it to Qwen3.8-Flash-Next on consumer hardware | Chapter 3, November digest, glossary PR 27 |
| [Basalt](https://github.com/jesdga95/basalt) | Inference engine | MIT | Self-hosted | Local engine aimed at NVIDIA Blackwell | Narrow hardware target | Chapter 3 |
| [hipfire](https://github.com/warpfront/hipfire) | Inference engine | Not stated | Self-hosted | RDNA-native Rust engine, pushed 25 Nov 2026 | No LICENSE file at the repository root | Chapter 3 |
| [TensorFold](https://github.com/ashhart/TensorFold) | Inference engine | Apache-2.0 | Self-hosted | Metal, CUDA, and Vulkan inference in one project | Young engine; no desktop product named in the repo description | Chapter 3 |
| [RamaLama](https://github.com/containers/ramalama) | Model runner | MIT | CLI, Self-hosted | Container-native model serving, pushed 23 Nov 2026 | Needs Podman or Docker | Chapter 3 and PR 26 |
| [KoboldCpp](https://github.com/LostRuins/koboldcpp) | Model runner | AGPL-3.0 | CLI, Desktop | Single binary with a local UI, pushed 25 Nov 2026 | AGPL duties if you serve a modified build | Chapter 3 |
| [Jan](https://github.com/janhq/jan) | Model runner | Apache-2.0 | Desktop | Offline desktop app; LICENSE file is Apache-2.0 | GitHub's detector does not emit an SPDX id | Chapter 3 |
| [textgen](https://github.com/oobabooga/textgen) | Model runner | AGPL-3.0 | Desktop | Local desktop app with an OpenAI/Anthropic-compatible API | Last push 17 Aug 2026 | Chapter 3 |
| [Open WebUI](https://github.com/open-webui/open-webui) | Model UI | Open WebUI License | Self-hosted | Web UI in front of Ollama or an OpenAI-compatible API | Branding clause: removing the name needs a small deployment, permission, or an enterprise license | Chapter 3 |
| [LocalAI](https://github.com/mudler/LocalAI) | Inference engine | MIT | Self-hosted | OpenAI-style local server for several model types, pushed 25 Nov 2026 | You operate the server and the hardware | Production runner found while checking local engines |
| [LM Studio](https://lmstudio.ai/) | Model runner | Proprietary | Desktop | Desktop app terms grant personal and internal business use | Those terms forbid resale, service-bureau use, and offering the app as SaaS | Chapter 3. [Omarchy manual](https://github.com/omacom/omarchy/blob/quattro/manual/17-ai.md) says to start here for local models |
| [Fireworks](https://fireworks.ai/) | Hosted inference | Not stated | SaaS | Token API he uses for open-weight models | License of the service is not stated on the sources read here | Used by DHH ([Lex #501 transcript](https://lexfridman.com/dhh-2-transcript/)). Omarchy's agents panel can store a Fireworks key for OpenCode |

## Agentic development environments

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [T3 Code](https://github.com/pingdotgg/t3code) | ADE | MIT | Desktop, Mobile, SaaS | README links a download, iOS, Android, and a web app | Drives agents you already have; it is not a model | Chapter 4 PR 28. Shipped in Omarchy ([manual](https://github.com/omacom/omarchy/blob/quattro/manual/17-ai.md)) |
| [Herdr](https://github.com/herdrdev/herdr) | ADE | Apache-2.0 | CLI, Desktop | Agent runtime, pushed 19 Nov 2026; Omarchy ships the CLI and the desktop app | Two install paths (package CLI and the app's own installer) | Used by DHH ([Lex #501 transcript](https://lexfridman.com/dhh-2-transcript/)). Chapter 4 PR 28. Shipped in Omarchy |
| [Orca](https://github.com/stablyai/orca) | ADE | MIT | Desktop, Mobile, Self-hosted | Repo description: desktop, mobile, and remote runtimes for a fleet of agents | No model of its own; you bring subscriptions | Chapter 4 PR 28 |
| [Conductor](https://www.conductor.build/) | ADE | Not stated | Desktop, Mobile, SaaS | Site: desktop, iOS, and an API; cloud sandboxes for Claude Code, Codex, Cursor, and OpenCode | Homepage states no license; product is "Conductor from Meta" | Chapter 4 PR 28. Changelog 0.100.0 is dated 24 Nov 2026 |
| [Nimbalyst](https://github.com/nimbalyst/nimbalyst) | ADE | MIT | Desktop, Mobile | README: desktop for macOS, Windows, and Linux, plus an iOS companion | Sessions run Codex, Claude Code, OpenCode, or another agent you attach | Chapter 4 PR 28 |
| [Claude Squad](https://github.com/smtg-ai/claude-squad) | ADE | AGPL-3.0 | CLI | Terminal app for several local agents in separate workspaces | README requires a local terminal workflow | Chapter 4 PR 28 |
| [Vibe Kanban](https://github.com/BloopAI/vibe-kanban) | ADE | Apache-2.0 | Desktop, Self-hosted | `npx vibe-kanban` locally; README also documents self-hosting | Cloud API settings exist; this pass did not confirm a public hosted plan's terms | Chapter 4 PR 28. Pushed 15 Nov 2026 |
| [Sculptor](https://github.com/imbue-ai/sculptor) | ADE | MIT | Desktop | README: desktop app for parallel coding agents | README says to treat it as an experimental research preview | Chapter 4 PR 28 |
| [SpyNEL](https://github.com/agent0ai/spynel) | Orchestrator | MIT | Not stated | One chat that drives other harnesses | Repository description does not name Desktop, Mobile, SaaS, or CLI | Chapter 4 and October digest |
| [Eigent](https://github.com/eigent-ai/eigent) | ADE | Apache-2.0 | Desktop | Description: open-source cowork desktop | Pushed 23 Nov 2026; still a young desktop | Chapter 4 harness table |
| [OpenHands](https://github.com/OpenHands/OpenHands) | ADE | MIT | Self-hosted | README: self-hosted control center for OpenHands and other ACP agents, including local and remote backends | The repo's product name on the README is Agent Canvas, not the old OpenDevin app | Chapter 4 |

## Coding agents and harnesses

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/overview) | Coding agent | Proprietary | CLI, Desktop, SaaS | Official docs: terminal, IDE, desktop app, and browser | `anthropics/claude-code` has no LICENSE file | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/); he drives with it and uses Agent View). Shipped in Omarchy |
| [Codex](https://github.com/openai/codex) | Coding agent | Apache-2.0 | CLI, Desktop, SaaS | README: local CLI, `codex app`, and Codex Web at chatgpt.com/codex | An OpenAI maintainer wrote that the desktop app is not open source | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/); review pass is Codex xHigh). January 2026 post also names "Codex 5" inside OpenCode ([blog](https://world.hey.com/dhh/promoting-ai-agents-3ee04945)). Shipped in Omarchy |
| [OpenCode](https://github.com/anomalyco/opencode) | Coding agent | MIT | CLI | Open-source coding agent, pushed 25 Nov 2026 | Repository description does not list a desktop or phone app | Used by DHH ([blog](https://world.hey.com/dhh/promoting-ai-agents-3ee04945) and [transcript](https://lexfridman.com/dhh-2-transcript/); his harness for open models). Shipped in Omarchy |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Coding agent | MIT | CLI, Desktop | Personal agent that keeps memory; Omarchy installs the desktop app and points `hermes` at it | Omarchy's copy updates with `hermes update`, not the distro package | Chapter 4. Shipped in Omarchy |
| [goose](https://github.com/aaif-goose/goose) | Coding agent | Apache-2.0 | CLI | Apache-2.0 agent under the Agentic AI Foundation; README badges a CLI package | Desktop app not stated in the README text read here | Chapter 4 and October digest |
| [OpenClaw](https://github.com/openclaw/openclaw) | Coding agent | MIT | CLI, Self-hosted | Gateway plus a terminal UI; Omarchy opens the control UI as a local web app | Removing it asks whether to keep `~/.openclaw`, which holds chats and credentials | Chapter 4. Shipped in Omarchy. Named, not claimed as his daily driver, in the [Basecamp post](https://world.hey.com/dhh/basecamp-becomes-agent-accessible-3ae6b949) |
| [Cline](https://github.com/cline/cline) | Coding agent | Apache-2.0 | CLI, Desktop | Description: SDK, IDE extension, or CLI | Pushed 23 Nov 2026 | Chapter 4 |
| [Agent Zero](https://github.com/agent0ai/agent-zero) | Coding agent | MIT | Not stated | Framework repo; LICENSE file is MIT even though GitHub's detector has no SPDX id | Description does not state Desktop, Mobile, or SaaS | Chapter 4 and October digest |
| [Pi](https://github.com/earendil-works/pi) | Coding agent | MIT | CLI | Description: agent toolkit with a TUI and a coding CLI | Omarchy opens local models in Pi even when another agent is the default | Shipped in Omarchy ([manual](https://github.com/omacom/omarchy/blob/quattro/manual/17-ai.md)) |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | Coding agent | Apache-2.0 | CLI | Terminal coding agent, pushed 25 Nov 2026 | Tuned around Alibaba's models | Shipped in Omarchy |
| [Kimi Code](https://github.com/MoonshotAI/kimi-code) | Coding agent | MIT | CLI | Moonshot's coding CLI, pushed 25 Nov 2026 | He named Kimi K3 as a model inside OpenCode, not this CLI as his driver | Shipped in Omarchy. Model use is in the models table |
| [Kilo Code](https://github.com/Kilo-Org/kilocode) | Coding agent | MIT | CLI | Open-source coding agent, pushed 25 Nov 2026 | Omarchy launches it as `kilo`; other surfaces are not stated in the repo description | Shipped in Omarchy |
| [Crush](https://github.com/charmbracelet/crush) | Coding agent | FSL-1.1-MIT | CLI | Charm's terminal coding agent, pushed 25 Nov 2026 | Functional Source License, not MIT, until the future-license date in that file | Shipped in Omarchy |
| [Mistral Vibe](https://github.com/mistralai/mistral-vibe) | Coding agent | Apache-2.0 | CLI | Description: minimal CLI coding agent, pushed 24 Nov 2026 | Omarchy's usage panel can show it; the launcher table does not list a `vibe` command | Production CLI, not a DHH-tagged tool |
| [GitHub Copilot](https://github.com/features/copilot) | Coding agent | Proprietary | CLI, SaaS | He uses Copilot review on pull requests; Omarchy ships the `copilot` CLI | `github/copilot-cli` has no SPDX id | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)). Shipped in Omarchy. January 2026 post says editor autocomplete, including Copilot, left him cold ([blog](https://world.hey.com/dhh/promoting-ai-agents-3ee04945)) |
| [Cursor](https://cursor.com/) | Coding agent | Proprietary | CLI | `cursor/cursor` publishes no license; Omarchy ships `cursor-agent` | Desktop and cloud surfaces are not restated from a Cursor docs page on this pass | Shipped in Omarchy. Editor autocomplete left him cold in January 2026; that post is not a claim he quit the CLI |
| [Grok Build](https://x.ai/) | Coding agent | Not stated | CLI | Omarchy installs a `grok` CLI through mise and warns against a second curl installer | No LICENSE file was found for the CLI | Shipped in Omarchy. He uses the Grok model (see models), including a review pass ([transcript](https://lexfridman.com/dhh-2-transcript/)) |
| [Kortix CompanyOS](https://github.com/kortix-ai/CompanyOS) | Agent harness | Elastic-2.0 | Self-hosted, SaaS | README: agents, skills, and memory in a git repo, with a cloud computer per agent | Elastic-2.0 is not an OSI license. `kortix-ai/suna` now resolves here. `kortix-ai/kortix` is 404 | Issue #14 and chapter 4 |

## Omarchy launchers whose license was not in a public LICENSE file

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [Antigravity CLI](https://antigravity.google/) | Coding agent | Not stated | CLI | Omarchy command `agy`; shortcut `ca` | License not stated in the manual | Shipped in Omarchy. His 23 Nov 2026 posts are about Gemini 4 Neon, not a sentence that names this binary |
| Amp | Coding agent | Not stated | CLI, Desktop | Manual: `amp` command and Amp Desktop under Install, AI | No upstream license read | Shipped in Omarchy |
| Command Code | Coding agent | Not stated | CLI | Manual command `commandcode` | Upstream site and license not confirmed | Shipped in Omarchy |
| Freebuff | Coding agent | Not stated | CLI | Manual: Codebuff's free, ad-supported agent, command `freebuff` | Manual says it takes no starting prompt | Shipped in Omarchy |
| [Devin CLI](https://devin.ai/) | Coding agent | Not stated | CLI | Manual command `devin`, from Cognition | License not stated | Shipped in Omarchy |
| Kiro CLI | Coding agent | Not stated | CLI | Manual command `kiro-cli` | License not stated | Shipped in Omarchy |
| MiniMax Code | Coding agent | Not stated | CLI | Manual command `mcode` | Manual: interactive sessions have no unattended permission mode | Shipped in Omarchy |
| Muse Code | Coding agent | Not stated | CLI | Manual command `muse`, Meta's coding agent | License not stated | Shipped in Omarchy |
| Oh My Pi | Coding agent | Not stated | CLI | Manual command `omp` | License not stated | Shipped in Omarchy |
| Ori | Coding agent | Not stated | CLI | Manual: `ori` runs other harnesses against OpenRouter, and `ori code` is its own agent | License not stated | Shipped in Omarchy |

## Not a stable release yet

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | Coding agent | MIT | CLI | Plugin-style harness, pushed 22 Nov 2026 | Newest GitHub releases that day are prerelease: `dsh-v0.2.3-alpha.2` and, before it, `dsh-v0.2.2-rc.5` | Shipped in Omarchy as `dsh`. Manual says official API use uploads session logs unless you turn that off |
| [Harness²](https://github.com/google-research/harness2) | Coding agent | Apache-2.0 | CLI, Self-hosted | Google Research harness for the Harness² paper; README shows a `harn` install path | No GitHub release or tag. Last push 2 Nov 2026 | Issue #7. Paper: [arXiv:2610.14224](https://arxiv.org/abs/2610.14224). Project page: [harness2.github.io](https://harness2.github.io/) |
| [dsh-superagent](https://github.com/deepseek-ai/dsh-superagent-prototype) | Coding agent | MIT | Self-hosted | README: a proactive coding agent for one GitHub repo, as a DeepSeek Harness bundle | README says research prototype, not an official product and not production-ready | Issue #16 and the November digest |

## Agent frameworks and SDKs

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [LangChain](https://github.com/langchain-ai/langchain) | Agent framework | MIT | Self-hosted | Agent-engineering library, pushed 25 Nov 2026 | Higher-level wrapper around model and tool calls | Issue #17 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Agent framework | MIT | Self-hosted | Library for stateful agent graphs, pushed 25 Nov 2026 | A library, not a coding product you install and chat with | Issue #17 |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | Agent framework | MIT | Self-hosted | README calls it a batteries-included harness on top of LangGraph, pushed 25 Nov 2026 | A Python package you embed, not a desktop app | Issue #17 |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Agent framework | MIT | Self-hosted | Role-based multi-agent framework, pushed 25 Nov 2026 | You write the orchestration | Production SDK |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Agent framework | MIT | Self-hosted | Typed Python agent library, pushed 25 Nov 2026 | Python-only | Production SDK |
| [smolagents](https://github.com/huggingface/smolagents) | Agent framework | Apache-2.0 | Self-hosted | Small library for agents that write code actions | Thin by design | Production SDK |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Agent framework | MIT | Self-hosted | Python SDK for multi-agent workflows, pushed 25 Nov 2026 | Separate from the Codex CLI | Production SDK |
| [Google ADK](https://github.com/google/adk-python) | Agent framework | Apache-2.0 | Self-hosted | Code-first Python agent toolkit, pushed 25 Nov 2026 | Python package, not the Antigravity app | Production SDK |
| [Mastra](https://github.com/mastra-ai/mastra) | Agent framework | Not stated | Self-hosted | TypeScript agent framework, pushed 25 Nov 2026 | LICENSE.md splits terms; an `ee/` tree is called out separately | Not a single SPDX id |

## MCP, skills, and agent-facing CLIs

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [FastMCP](https://github.com/PrefectHQ/fastmcp) | MCP library | Apache-2.0 | Self-hosted | Python library for MCP servers and clients | `jlowin/fastmcp` now resolves to this PrefectHQ repo | Production library |
| [Honcho](https://github.com/plastic-labs/honcho) | Agent memory | AGPL-3.0 | Self-hosted | Memory library for stateful agents, pushed 24 Nov 2026 | AGPL if you serve a modified copy | October digest |
| [DOX](https://github.com/agent0ai/dox) | Project context | MIT | CLI | AGENTS.md hierarchy for coding agents | Last push 1 Sep 2026 | Chapter 4, October digest, and issue #9 |
| [Skillsync](https://skillsync.com/) | Skill library | Proprietary | SaaS | Hosted skill library with an MCP connector at app.skillsync.com/mcp for Claude, ChatGPT, and Cursor | Terms (23 Nov 2026): skills are not reviewed before publish, and selling is by invitation | Issue #24 |
| [Basecamp CLI](https://github.com/basecamp/basecamp-cli) | Agent CLI | MIT | CLI, SaaS | Official CLI plus agent skills; the service it calls is Basecamp | Needs a Basecamp account | Used by DHH ([post](https://x.com/dhh/status/2125498388385022313), 25 Nov 2026: he drives much of his Basecamp use with agents). Shipped by 37signals ([blog](https://world.hey.com/dhh/basecamp-becomes-agent-accessible-3ae6b949)) |
| [HEY CLI](https://github.com/basecamp/hey-cli) | Agent CLI | MIT | CLI, SaaS | CLI and TUI for HEY, including `hey setup` for Claude Code and Codex | Needs a HEY account | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/): an Omarchy bot emails him through the HEY CLI) |

## Evals and observability

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [promptfoo](https://github.com/promptfoo/promptfoo) | Evals | MIT | CLI, Self-hosted | Prompt, agent, and RAG tests, pushed 25 Nov 2026 | You supply the cases | Production eval runner |
| [DeepEval](https://github.com/confident-ai/deepeval) | Evals | Apache-2.0 | Self-hosted | LLM evaluation framework, pushed 25 Nov 2026 | A library, not a hosted board | Production eval library |
| [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) | Evals | MIT | Self-hosted | UK AISI evaluation framework, pushed 25 Nov 2026 | You run the evals | Production eval framework |
| [SWE-bench](https://github.com/SWE-bench/SWE-bench) | Evals | MIT | Self-hosted | Real GitHub-issue benchmark harness | Last push 18 Sep 2026 | Chapter 2 names the benchmark |
| [Phoenix](https://github.com/Arize-ai/phoenix) | Observability | Elastic-2.0 | Self-hosted | Tracing and evaluation app, pushed 25 Nov 2026 | Elastic License 2.0, not OSI open source | Production observability |
| [Langfuse](https://github.com/langfuse/langfuse) | Observability | Not stated | Self-hosted | Tracing, evals, and prompt management, pushed 25 Nov 2026 | LICENSE splits enterprise paths out of the main grant | Not a single SPDX id |
| [LangSmith](https://github.com/langchain-ai/langsmith-python) | Observability | MIT | Self-hosted, SaaS | Python and JavaScript SDKs, both pushed 25 Nov 2026; docs live at docs.smith.langchain.com | The combined `langsmith-sdk` repo was archived on 16 Oct 2026 | Issue #17. SDK license is MIT; hosted-product terms were not read |

## Sandboxes and agent runtimes

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [Docker CLI](https://github.com/docker/cli) | Sandbox | Apache-2.0 | CLI, Self-hosted | The usual container boundary for an agent shell | Isolation is only as tight as the daemon and mounts | Chapter 4 |
| [Podman](https://github.com/containers/podman) | Sandbox | Apache-2.0 | CLI, Self-hosted | Rootless containers; Omarchy runs its local models here | Manual: a model holds most of the machine's memory while it runs | Shipped in Omarchy ([manual](https://github.com/omacom/omarchy/blob/quattro/manual/17-ai.md)) |
| [E2B](https://github.com/e2b-dev/E2B) | Sandbox | Apache-2.0 | Self-hosted, SaaS | Secure environments for agents, pushed 25 Nov 2026 | Hosted and self-hosted are different operating jobs | Chapter 4 and October digest |
| [OpenShell](https://github.com/ai-openshell/openshell) | Sandbox | Apache-2.0 | Self-hosted | Safe runtime for autonomous agents, pushed 25 Nov 2026 | A runtime you deploy, not a chat app | October digest and issue #4. `NVIDIA/OpenShell` resolves to `ai-openshell/openshell` |
| [NemoClaw](https://github.com/NVIDIA/NemoClaw) | Sandbox | Apache-2.0 | CLI, Self-hosted | NVIDIA packaging for Hermes and other agents on OpenShell | Opinionated about that sandbox | November digest and issue #6 |
| [Orgo](https://www.orgo.ai/) | Sandbox | Proprietary | SaaS | Cloud Linux and Windows desktops for agents, with an API and a hosted MCP server | Paid plans; `orgo.dev` did not answer on this pass | Issue #12. The November digest links orgo.dev |
| [Tuxee](https://github.com/agent0ai/tuxee) | Sandbox | MIT | Self-hosted | Small Linux environment for servers and agents; LICENSE file is MIT | GitHub's detector has no SPDX id | November digest |

## Terminal tools in DHH's workflow

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [Ghostty](https://github.com/ghostty-org/ghostty) | Terminal | MIT | Desktop | GPU terminal with native UI on each platform | A terminal, not an agent | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)) |
| [tmux](https://github.com/tmux/tmux) | Terminal | ISC | CLI | Sessions and panes; he started parallel agents here | He says it was not enough once agents spanned machines | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)). Shipped in Omarchy |
| [Neovim](https://github.com/neovim/neovim) | Editor | Apache-2.0 | CLI | He uses it as a project browser while agents edit | LICENSE keeps the Vim license on parts that arrived under it | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)) |
| [lazygit](https://github.com/jesseduffield/lazygit) | Git UI | MIT | CLI | Terminal UI he launches from Neovim to read the change log | Shows git state; it does not run the agent | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)) |
| [mise](https://github.com/jdx/mise) | Tool installer | MIT | CLI | He uses it to install agent CLIs that update many times a day | Not an agent | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)). Omarchy installs most agents through it |
| [Hunk](https://github.com/modem-dev/hunk) | Diff reviewer | MIT | CLI | Review-first terminal diffs with an agent skill | He said he still wants surrounding files, so Neovim stays in the loop | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)). His fork [dhh/hunk](https://github.com/dhh/hunk) points at this project |

## Desktop chat apps Omarchy installs

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| ChatGPT desktop | Chat app | Not stated | Desktop | Omarchy Install, AI entry | License not stated in the manual | Shipped in Omarchy. Distinct from the Codex CLI |
| Perplexity desktop | Chat app | Not stated | Desktop | Omarchy Install, AI entry | License not stated in the manual | Shipped in Omarchy |
| Grok Bot | Chat app | Not stated | Desktop | Manual: desktop chat app, separate from the `grok` coding CLI | License not stated in the manual | Shipped in Omarchy. He suggested pairing a laptop with a Grok bot for remote work ([post](https://x.com/dhh/status/2110503544063488177), 14 Oct 2026) |

## Models he says he runs

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [Claude Opus and Fable](https://claude.com/) | Model | Not stated | SaaS | On 23 Nov 2026 he ranked Opus 5.5 first, ahead of Gemini 4 Neon | A long Fable job burned a Max window and fell through to Opus 5 | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/), [post](https://x.com/dhh/status/2124863854828233196), [January blog](https://world.hey.com/dhh/promoting-ai-agents-3ee04945) for Opus 4.5) |
| [GPT Sol](https://openai.com/) | Model | Not stated | SaaS | Finished the same Rust translation; on 13 Oct 2026 he posted it within 5 points of Opus at under a tenth of the token cost | GPT Luna did not finish that translation and tried to wrap an existing implementation | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/), [post](https://x.com/dhh/status/2110148376755097938)) |
| [Gemini 4 Neon](https://deepmind.google/) | Model | Not stated | SaaS | He ran it across six computers in one day and did not exhaust the session window | Same-day post: the harness is rough and lacks Claude's agent overview | Used by DHH ([post](https://x.com/dhh/status/2124860839572488538), [post](https://x.com/dhh/status/2124949501534171477)) |
| Gemini 3 | Model | Not stated | SaaS | Named in January 2026 among models he ran in OpenCode | No November 2026 post read here says he still uses Gemini 3 | Used by DHH ([blog](https://world.hey.com/dhh/promoting-ai-agents-3ee04945)) |
| Grok 4.6 | Model | Not stated | SaaS | Completed the Rust translation he also gave Fable and Sol | He said Grok 4.5 felt too far behind to keep using | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)) |
| Kimi K3 | Model | Not stated | SaaS | Open model he runs through OpenCode on Fireworks | He said that translation run took a long time | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)) |
| MiniMax M2.1 | Model | Not stated | SaaS | Named in January 2026 as an open-weight model he put to work in OpenCode | The January post does not say he still uses it in November | Used by DHH ([blog](https://world.hey.com/dhh/promoting-ai-agents-3ee04945)) |
| GLM-4.7 | Model | Not stated | SaaS | Named in that same January list | No later post read here repeats it | Used by DHH ([blog](https://world.hey.com/dhh/promoting-ai-agents-3ee04945)) |
| DeepSeek V4 | Model | Not stated | SaaS | V4 Pro finished the Rust translation | V4 Flash failed it, in the same way Luna did | Used by DHH ([transcript](https://lexfridman.com/dhh-2-transcript/)) |

## Local machine and other issue tools

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [gputaskman](https://github.com/shanselman/gputaskman) | GPU monitor | MIT | CLI | Per-process VRAM and LLM buffer breakdown on Windows, Linux, WSL, and macOS | README calls it early experimental software; model breakdowns are estimates | Issue #23. Release v0.4.5 is dated 21 Nov 2026 |
| [ArtCraft Launcher](https://github.com/storytold/craft-launcher) | App launcher | Apache-2.0 | Desktop | Installs and opens the Craft app suite. Stable release v0.20.1 on 25 Nov 2026 | A creative-suite launcher, not a coding agent | Issue #22. The issue link is the older tag v0.19.2. Site: [getartcraft.com](https://getartcraft.com/) |

## AI code review

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [Greptile](https://www.greptile.com/) | AI code review | Proprietary | SaaS, Self-hosted | Reviews pull requests on GitHub, GitLab, Bitbucket, and other hosts using codebase context | Self-hosting requires an Enterprise license; cloud reviews spend credits | Docs: https://www.greptile.com/docs/quickstart . No public source repo found at greptileai/greptile |
| [CodeRabbit](https://www.coderabbit.ai/) | AI code review | Proprietary | SaaS, Self-hosted | GitHub App that reviews pull requests; the marketplace says public repositories are free | Terms call the service proprietary and reserve the product IP. A separate skills repo is MIT and is not this product | Terms: https://tos.coderabbit.ai/ . Marketplace: https://github.com/marketplace/coderabbitai |
| [Graphite Agent](https://graphite.com/docs/ai-reviews) | AI code review | Not stated | SaaS | Automatically reviews new pull requests and posts a comment with a suggested fix | Docs do not name a source license. A pull request over 200,000 characters is not analyzed | A June 2025 Graphite status incident still names Diamond as the AI code reviewer: https://status.graphite.com/cmbtsj3sp009i14elpd3zj1v0 |
| [PR-Agent](https://github.com/The-PR-Agent/pr-agent) | AI code review | MIT | Self-hosted | Community-maintained open-source pull-request reviewer, pushed 25 Nov 2026 | README says this is not Qodo's hosted review product | Docs: https://www.pr-agent.ai |
| [Qodo](https://www.qodo.ai/ai-code-review-platform/) | AI code review | Proprietary | SaaS, Self-hosted | Reviews pull requests inside Git; Qodo Merge was folded into this platform | Business terms license the hosted platform for internal use. Enterprise pricing lists on-prem and air-gapped installs | Former name: https://www.qodo.ai/formerly-qodo-merge/ . Terms: https://www.qodo.ai/business-terms-of-service/ |
| [Cursor Bugbot](https://cursor.com/docs/bugbot) | AI code review | Proprietary | SaaS | Reviews pull-request diffs on GitHub, GitLab, Bitbucket, Azure DevOps, and Origin, and posts fix suggestions | Skips a pull request over its size limit. Docs do not publish a source license | The cursor/cursor repository lists no license |
| [GitHub Copilot code review](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-code-review) | AI code review | Proprietary | SaaS | Reviews a GitHub pull request and can suggest changes you apply in the pull request | Automatic review depends on the Copilot plan. A default review is a comment, not an approval | Distinct from the Copilot CLI row |
| [Sourcery](https://github.com/sourcery-ai/sourcery) | AI code review | MIT | SaaS | GitHub App that reviews a pull request with a summary and line comments | Getting started is the hosted GitHub App. The README does not describe a self-hosted server | Install: https://github.com/apps/sourcery-ai/installations/new . Repo pushed 10 Nov 2026 |

## Agent security

| Tool | Category | License | Platform | Strength | Limitation | Note |
| --- | --- | --- | --- | --- | --- | --- |
| [Nightwatch](https://huggingface.co/docs/hub/en/enterprise-nightwatch) | Agent security | Proprietary | SaaS | Security agent scans Hugging Face Hub activity logs in real time and alerts Slack or an incident system | Paid Enterprise add-on only. The docs do not publish a source license or a price | Official Hub docs. No huggingface GitHub repo named nightwatch |
