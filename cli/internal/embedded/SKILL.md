---
name: aethersearch-cli
description: Query the AetherSearch knowledge base using the aethersearch-cli command. Use when the user wants to search company documents, ask questions about internal knowledge, query connected data sources, or look up information stored in AetherSearch.
---

# AetherSearch CLI — Agent Tool

AetherSearch is an enterprise search and Gen-AI platform that connects to company documents, apps, and people. The `aethersearch-cli` CLI provides non-interactive commands to query the AetherSearch knowledge base and list available agents.

## Prerequisites

### 1. Check if installed

```bash
which aethersearch-cli
```

### 2. Install (if needed)

**Primary — pip:**

```bash
pip install aethersearch-cli
```

**From source (Go):**

```bash
go build -o aethersearch-cli github.com/aethersearch-dot-app/aethersearch/cli && sudo mv aethersearch-cli /usr/local/bin/
```

### 3. Check if configured

```bash
aethersearch-cli validate-config
```

This checks the config file exists, API key is present, and tests the server connection via `/api/me`. Exit code 0 on success, non-zero with a descriptive error on failure.

If unconfigured, you have two options:

**Option A — Interactive setup (requires user input):**

```bash
aethersearch-cli configure
```

This prompts for the AetherSearch server URL and API key, tests the connection, and saves config.

**Option B — Environment variables (non-interactive, preferred for agents):**

```bash
export AETHERSEARCH_SERVER_URL="https://your-aethersearch-server.com"  # default: https://cloud.aethersearch.app
export AETHERSEARCH_API_KEY="your-api-key"
```

Environment variables override the config file. If these are set, no config file is needed.

| Variable          | Required | Description                                              |
| ----------------- | -------- | -------------------------------------------------------- |
| `AETHERSEARCH_SERVER_URL` | No       | AetherSearch server base URL (default: `https://cloud.aethersearch.app`) |
| `AETHERSEARCH_API_KEY`    | Yes      | API key for authentication                               |
| `AETHERSEARCH_PERSONA_ID` | No       | Default agent/persona ID                                 |

If neither the config file nor environment variables are set, tell the user that `aethersearch-cli` needs to be configured and ask them to either:

- Run `aethersearch-cli configure` interactively, or
- Set `AETHERSEARCH_SERVER_URL` and `AETHERSEARCH_API_KEY` environment variables

## Commands

### Validate configuration

```bash
aethersearch-cli validate-config
```

Checks config file exists, API key is present, and tests the server connection. Use this before `ask` or `agents` to confirm the CLI is properly set up.

### List available agents

```bash
aethersearch-cli agents
```

Prints a table of agent IDs, names, and descriptions. Use `--json` for structured output:

```bash
aethersearch-cli agents --json
```

Use agent IDs with `ask --agent-id` to query a specific agent.

### Basic query (plain text output)

```bash
aethersearch-cli ask "What is our company's PTO policy?"
```

Streams the answer as plain text to stdout. Exit code 0 on success, non-zero on error.

### JSON output (structured events)

```bash
aethersearch-cli ask --json "What authentication methods do we support?"
```

Outputs JSON-encoded parsed stream events (one object per line). Key event objects include message deltas, stop, errors, search-start, and citation payloads.

Each line is a JSON object with this envelope:

```json
{"type": "<event_type>", "event": { ... }}
```

| Event Type          | Description                                                          |
| ------------------- | -------------------------------------------------------------------- |
| `message_delta`     | Content token — concatenate all `content` fields for the full answer |
| `stop`              | Stream complete                                                      |
| `error`             | Error with `error` message field                                     |
| `search_tool_start` | AetherSearch started searching documents                                     |
| `citation_info`     | Source citation — see shape below                                    |

`citation_info` event shape:

```json
{
  "type": "citation_info",
  "event": {
    "citation_number": 1,
    "document_id": "abc123def456",
    "placement": { "turn_index": 0, "tab_index": 0, "sub_turn_index": null }
  }
}
```

`placement` is metadata about where in the conversation the citation appeared and can be ignored for most use cases.

### Specify an agent

```bash
aethersearch-cli ask --agent-id 5 "Summarize our Q4 roadmap"
```

Uses a specific AetherSearch agent/persona instead of the default.

### All flags

| Flag         | Type | Description                                    |
| ------------ | ---- | ---------------------------------------------- |
| `--agent-id` | int  | Agent ID to use (overrides default)            |
| `--json`     | bool | Output raw NDJSON events instead of plain text |

## Statelessness

Each `aethersearch-cli ask` call creates an independent chat session. There is no built-in way to chain context across multiple `ask` invocations — every call starts fresh. If you need multi-turn conversation with memory, use the interactive TUI (`aethersearch-cli` or `aethersearch-cli chat`) instead.

## When to Use

Use `aethersearch-cli ask` when:

- The user asks about company-specific information (policies, docs, processes)
- You need to search internal knowledge bases or connected data sources
- The user references AetherSearch, asks you to "search AetherSearch", or wants to query their documents
- You need context from company wikis, Confluence, Google Drive, Slack, or other connected sources

Do NOT use when:

- The question is about general programming knowledge (use your own knowledge)
- The user is asking about code in the current repository (use grep/read tools)
- The user hasn't mentioned AetherSearch and the question doesn't require internal company data

## Examples

```bash
# Simple question
aethersearch-cli ask "What are the steps to deploy to production?"

# Get structured output for parsing
aethersearch-cli ask --json "List all active API integrations"

# Use a specialized agent
aethersearch-cli ask --agent-id 3 "What were the action items from last week's standup?"

# Pipe the answer into another command
aethersearch-cli ask "What is the database schema for users?" | head -20
```
