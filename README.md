<a name="readme-top"></a>

<h2 align="center">
    <img width="50%" src="/assets/logo-aethersearch.png" alt="AetherSearch Logo" />
</h2>

<p align="center">
    <a href="https://github.com/vishalm/ai-enterprise-search-chat-onyx/blob/main/LICENSE" target="_blank">
        <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=blue" alt="License" />
    </a>
</p>

# AetherSearch — Enterprise AI Search & Agentic Knowledge Platform

**AetherSearch** is the application layer for LLMs — a feature-rich, self-hostable enterprise AI platform that brings advanced capabilities like RAG, web search, code execution, file creation, deep research, and agentic workflows to your organization.

Connect your applications with over 50+ indexing-based connectors provided out of the box or via MCP.

---

## Features

- **Agentic RAG:** Best-in-class search and answer quality based on hybrid index + AI Agents for information retrieval.
- **Deep Research:** In-depth reports with a multi-step research flow.
- **Custom Agents:** Build AI Agents with unique instructions, knowledge, and actions.
- **Web Search:** Browse the web for up-to-date information. Supports Serper, Google PSE, Brave, SearXNG, and others.
- **Artifacts:** Generate documents, graphics, and other downloadable artifacts.
- **Actions & MCP:** Let agents interact with external applications, with flexible auth options.
- **Code Execution:** Execute code in a sandbox to analyze data, render graphs, or modify files.
- **Voice Mode:** Chat via text-to-speech and speech-to-text.
- **Image Generation:** Generate images based on user prompts.

AetherSearch supports all major LLM providers, both self-hosted (Ollama, LiteLLM, vLLM, etc.) and proprietary (Anthropic, OpenAI, Gemini, etc.).

---

## Deployment Modes

AetherSearch supports deployments in Docker, Kubernetes, Helm/Terraform and provides guides for major cloud providers.

### AetherSearch Lite

A lightweight Chat UI mode requiring fewer resources (under 1GB memory) and a less complex stack. Great for quick evaluation or teams interested only in Chat UI and Agents.

### Standard AetherSearch

The complete feature set, recommended for serious users and larger teams. Includes:
- Vector + Keyword index for RAG
- Background containers for job queues and workers to sync knowledge from connectors
- AI model inference servers for deep learning models used during indexing and inference
- Performance optimizations for large scale use via in-memory cache (Redis) and blob store (MinIO)

---

## AetherSearch for Enterprise

Built for teams of all sizes, from individual users to the largest global enterprises:

- **Collaboration:** Share chats and agents across your organization.
- **Single Sign-On:** SSO via Google OAuth, OIDC, or SAML. Group syncing and user provisioning via SCIM.
- **Role-Based Access Control:** RBAC for sensitive resources like agents, actions, and more.
- **Analytics:** Usage graphs broken down by teams, LLMs, or agents.
- **Query History:** Audit usage to ensure safe AI adoption.
- **Custom Code:** Run custom code to remove PII, reject sensitive queries, or run custom analysis.
- **Whitelabeling:** Customize the look and feel with custom naming, icons, banners, and more.

---

## Licensing

There are two editions of AetherSearch:

- **AetherSearch Community Edition (CE)** is available freely under the MIT license and covers all core features for Chat, RAG, Agents, and Actions.
- **AetherSearch Enterprise Edition (EE)** includes extra features primarily useful for larger organizations.

---

## Contributing

Looking to contribute? Please check out the [Contribution Guide](CONTRIBUTING.md) for more details.
