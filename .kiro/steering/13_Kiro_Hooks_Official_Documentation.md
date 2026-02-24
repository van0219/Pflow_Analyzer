---
inclusion: manual
---

# Kiro Hooks Reference

Official AWS documentation for Kiro Agent Hooks - automated triggers that execute predefined actions when specific IDE events occur.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Core Concepts](#core-concepts)
- [Event Types](#event-types)
- [Action Types](#action-types)
- [Hook Schema](#hook-schema)
- [Creating Hooks](#creating-hooks)
- [Management Operations](#management-operations)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

## Quick Reference

### When to Use Hooks

| Use Case | Event Type | Action Type |
|----------|------------|-------------|
| Validate before operations | `preToolUse` | `runCommand` (can block) |
| Review after changes | `agentStop`, `postToolUse` | `askAgent` |
| Maintain code quality | `fileEdited` | `askAgent` or `runCommand` |
| Generate boilerplate | `fileCreated` | `askAgent` |
| Clean up resources | `fileDeleted` | `askAgent` |
| On-demand tasks | `userTriggered` | `askAgent` |
| Log/audit operations | `promptSubmit`, `postToolUse` | `runCommand` |

### Event Type Decision Matrix

```
Need to block operations? → preToolUse (shell command with exit code)
Need to review agent work? → agentStop (agent prompt)
Need to process file changes? → fileEdited/fileCreated/fileDeleted
Need manual control? → userTriggered
Need to log/audit? → promptSubmit, postToolUse (shell command)
```

## Core Concepts

### What Are Hooks

Hooks automate workflows by executing actions when IDE events occur. Two-step process:
1. **Event Detection** - System monitors for specific events
2. **Automated Action** - Execute agent prompt or shell command

### Key Benefits

- Maintain consistent code quality
- Prevent security vulnerabilities  
- Reduce manual overhead
- Standardize team processes
- Create faster development cycles

### Hook Execution Flow

```
Event Occurs → Hook Triggered → Action Executed → Result Applied
```

**Special Cases:**
- `preToolUse` + shell command with exit code ≠ 0 → **BLOCKS** tool execution
- `promptSubmit` + shell command with exit code ≠ 0 → **BLOCKS** prompt submission
- `promptSubmit` + agent prompt → Prompt **APPENDED** to user message (not separate)

## Event Types

### File Events

#### fileEdited
**Triggers:** When files matching patterns are saved

**Configuration:**
```json
{
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.ts", "!**/*.test.ts"]
  }
}
```

**Use Cases:** Linting, formatting, test generation, documentation updates

---

#### fileCreated
**Triggers:** When new files matching patterns are created

**Configuration:**
```json
{
  "when": {
    "type": "fileCreated",
    "patterns": ["src/components/**/*.tsx"]
  }
}
```

**Use Cases:** Boilerplate generation, license headers, test file creation

---

#### fileDeleted
**Triggers:** When files matching patterns are deleted

**Configuration:**
```json
{
  "when": {
    "type": "fileDeleted",
    "patterns": ["src/**/*.ts"]
  }
}
```

**Use Cases:** Clean up related files, update imports, maintain project integrity

---

### Agent Events

#### promptSubmit
**Triggers:** When user submits a prompt

**Special Features:**
- Shell commands can access `$USER_PROMPT` environment variable
- Agent prompts are **APPENDED** to user prompt (not sent separately)

**Configuration:**
```json
{
  "when": {
    "type": "promptSubmit"
  }
}
```

**Use Cases:** Add context, block certain prompts, log prompts, validate input

---

#### agentStop
**Triggers:** When agent completes its turn

**Configuration:**
```json
{
  "when": {
    "type": "agentStop"
  }
}
```

**Use Cases:** Compile code, format generated code, review changes, run tests

---

### Tool Events

#### preToolUse
**Triggers:** Before agent invokes a tool

**Special Feature:** Shell commands with exit code ≠ 0 **BLOCK** tool execution

**Configuration:**
```json
{
  "when": {
    "type": "preToolUse",
    "toolTypes": ["write", "@mcp.*sql.*"]
  }
}
```

**Tool Type Filters:**
- Built-in categories: `read`, `write`, `shell`, `web`, `spec`, `*`
- Prefix filters: `@mcp`, `@powers`, `@builtin`
- Regex patterns: `@mcp.*sql.*` (matches MCP tools with "sql" in name)

**Use Cases:** Access control, validation, provide additional context

---

#### postToolUse
**Triggers:** After agent invokes a tool

**Configuration:**
```json
{
  "when": {
    "type": "postToolUse",
    "toolTypes": ["write"]
  }
}
```

**Use Cases:** Log tool invocations, format files, review changes, provide feedback

---

### Task Events

#### preTaskExecution
**Triggers:** Before spec task status changes to `in_progress`

**Configuration:**
```json
{
  "when": {
    "type": "preTaskExecution"
  }
}
```

**Use Cases:** Setup scripts, validate prerequisites, log task start

---

#### postTaskExecution
**Triggers:** After spec task status changes to `completed`

**Configuration:**
```json
{
  "when": {
    "type": "postTaskExecution"
  }
}
```

**Use Cases:** Run tests, lint/format, generate docs, notify external systems

---

### Manual Events

#### userTriggered
**Triggers:** Manual execution only

**Configuration:**
```json
{
  "when": {
    "type": "userTriggered"
  }
}
```

**Execution:** Click play button (▷) in Agent Hooks panel or "Start Hook" button

**Use Cases:** On-demand code reviews, documentation generation, security scans

---

## Action Types

### Agent Prompt (askAgent)

**Description:** Sends prompt to agent, triggers full agent loop

**Configuration:**
```json
{
  "then": {
    "type": "askAgent",
    "prompt": "Your instructions to the agent"
  }
}
```

**Characteristics:**
- ✓ Context-aware (uses current agent context)
- ✓ Can make decisions and perform complex tasks
- ✓ Natural language instructions
- ✗ Slower (uses LLM)
- ✗ Consumes credits

**When to Use:**
- Need natural language instructions
- Action depends on current context
- Need agent to make decisions
- Complex reasoning or analysis required

---

### Shell Command (runCommand)

**Description:** Executes shell command locally

**Configuration:**
```json
{
  "then": {
    "type": "runCommand",
    "command": "your shell command here",
    "timeout": 60
  }
}
```

**Exit Code Behavior:**
- Exit 0: stdout added to agent context, operation continues
- Exit ≠ 0: stderr sent to agent, agent notified of error
- Exit ≠ 0 + `preToolUse`: **BLOCKS** tool execution
- Exit ≠ 0 + `promptSubmit`: **BLOCKS** prompt submission

**Timeout:**
- Default: 60 seconds
- Set to 0 to disable timeout

**Characteristics:**
- ✓ Fast (executes locally)
- ✓ No credit consumption
- ✓ Can block operations (preToolUse, promptSubmit)
- ✓ Deterministic execution
- ✗ Not context-aware
- ✗ Cannot make decisions

**When to Use:**
- Have specific command to run
- Action is deterministic
- Need fast execution
- Want to avoid credit consumption
- Need to validate/block operations

---

## Hook Schema

### Complete Schema

```json
{
  "enabled": true,
  "name": "Hook Name",
  "description": "What the hook does",
  "version": "1",
  "when": {
    "type": "eventType",
    "patterns": ["*.ts", "*.tsx"],
    "toolTypes": ["write", "@mcp.*sql.*"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Instructions for the agent",
    "timeout": 60
  }
}
```

### Required Fields

- `name` (string) - Hook name
- `version` (string) - **MUST be string, not number** (IDE requirement)
- `when.type` (string) - Event type
- `then.type` (string) - Action type ("askAgent" or "runCommand")
- `then.prompt` (string) - Required for askAgent
- `then.command` (string) - Required for runCommand

### Optional Fields

- `enabled` (boolean) - Default: true
- `description` (string) - Hook description
- `when.patterns` (array) - Required for file events
- `when.toolTypes` (array) - Required for preToolUse/postToolUse
- `then.timeout` (number) - Default: 60 seconds (runCommand only)

### Validation Rules

1. `version` must be string type (e.g., "1" not 1)
2. File events require `when.patterns`
3. Tool events require `when.toolTypes`
4. askAgent requires `then.prompt`
5. runCommand requires `then.command`

**Validation Tool:** `python ReusableTools/validate_json.py <hook_file>`

---

## Creating Hooks

### Method 1: Ask Kiro (Natural Language)

1. Open Agent Hooks panel in Kiro
2. Click + button
3. Select "Ask Kiro to create a hook"
4. Describe workflow in natural language
5. Review generated configuration
6. Click Save Hook

**Best For:** Complex hooks, when unsure of exact configuration

---

### Method 2: Manual Creation (Form-Based)

1. Open Agent Hooks panel in Kiro
2. Click + button
3. Select "Manually create a hook"
4. Fill form fields:
   - Title (name)
   - Description
   - Event (when.type)
   - Tool name (when.toolTypes) - for tool events
   - File pattern (when.patterns) - for file events
   - Action (then.type)
   - Instructions/Command (then.prompt or then.command)
5. Click Create Hook

**Best For:** Simple hooks, when you know exact configuration

---

### Alternative Access

Command Palette: `Kiro: Open Kiro Hook UI`
- Mac: `Cmd + Shift + P`
- Windows/Linux: `Ctrl + Shift + P`

---

## Management Operations

### Enable/Disable

**Quick Toggle:** Click eye icon (👁️) in Agent Hooks panel

**Detailed Toggle:** Select hook → "Hook Enabled" switch in top-right

**JSON Field:** `enabled: true` or `enabled: false`

**Use Cases:** Temporarily disable during debugging, conditional automation

---

### Edit

1. Select hook in Agent Hooks panel
2. Modify any field (event type, patterns, instructions, etc.)
3. Changes apply immediately (no save button)

**Editable Fields:** All fields except file location

---

### Delete

1. Select hook in Agent Hooks panel
2. Click "Delete Hook" at bottom
3. Confirm deletion

**Warning:** Cannot be undone. Consider disabling instead.

---

### Run Manual Trigger

**Quick Run:** Click play button (▷) next to hook name

**Detailed Run:** Select hook → "Start Hook" button in top-right

**Applies To:** Only `userTriggered` hooks

---

### Programmatic Management

**Tools:**
- `ReusableTools/hook_manager.py` - 11 commands (backup, restore, validate, etc.)
- `ReusableTools/validate_json.py` - JSON validation with hook detection

**When to Use:**
- Long sessions (avoid fsWrite context issues)
- Batch operations
- Automated generation/updates
- CI/CD integration
- Backup and restore

**Critical Rule:** In long sessions (10+ messages), ALWAYS use `hook_manager.py` for hook editing, NEVER fsWrite or file-writer-helper.

---

## Best Practices

### Hook Design

#### Be Specific and Clear

**Good:**
```
When a TypeScript file is saved:
1. Check for unused imports
2. Remove them if found
3. Report the changes made
```

**Bad:**
```
Fix the file
```

#### One Task Per Hook

Don't combine multiple responsibilities. Create separate hooks for separate concerns.

#### Test Thoroughly

**Testing Checklist:**
- ✓ Normal case (expected input)
- ✓ Edge cases (empty files, large files, special characters)
- ✓ Error cases (malformed input, missing dependencies)
- ✓ Performance (doesn't slow down workflow)

#### Start Small

Begin with limited file patterns, expand after testing:
```
Start:  patterns: ["src/components/Button.tsx"]
Test:   patterns: ["src/components/*.tsx"]
Expand: patterns: ["src/**/*.tsx"]
```

---

### Security

#### Validate Inputs

**Shell Command Example:**
```bash
#!/bin/bash
if [ -z "$USER_PROMPT" ]; then
    echo "Error: No prompt provided" >&2
    exit 1
fi
# Sanitize input
SAFE_PROMPT=$(echo "$USER_PROMPT" | sed 's/[^a-zA-Z0-9 ]//g')
```

#### Limit Scope

**Specific Patterns:**
```
❌ Bad:  patterns: ["*"]
✓ Good: patterns: ["src/**/*.ts", "!src/**/*.test.ts"]
```

#### Review Regularly

**Review Checklist:**
- Are all hooks still relevant?
- Are prompts still accurate?
- Are file patterns still appropriate?
- Are there new use cases to automate?

---

### Performance

#### Monitor Frequency

Avoid hooks on high-frequency events:
```
❌ Bad:  fileEdited on every file save
✓ Good: agentStop or userTriggered for expensive operations
```

#### Optimize Prompts

Keep agent instructions concise (<200 words)

#### Use Shell Commands When Possible

Shell commands are faster and don't consume credits for deterministic tasks.

#### Set Appropriate Timeouts

```json
{
  "then": {
    "type": "runCommand",
    "command": "quick-command",
    "timeout": 10
  }
}
```

---

### Team Collaboration

#### Document Hooks

```json
{
  "name": "TypeScript Linter",
  "description": "Runs ESLint on TypeScript files after save. 
                  Requires ESLint to be installed. 
                  May take 2-3 seconds for large files.",
  "version": "1"
}
```

#### Version Control

- Commit `.kiro/hooks/*.kiro.hook` files to Git
- Document hooks in team README
- Review hook changes in pull requests

#### Create Standard Hooks

Common team workflows:
- Code formatting on save
- Security scanning before commit
- Test coverage checks
- Documentation generation

---

## Troubleshooting

### Hook Not Triggering

**Check:**
1. File pattern matches target files
   - `*.ts` won't match `*.tsx` - use `*.{ts,tsx}`
2. Hook is enabled (eye icon 👁️ in panel)
3. Event type is correct
   - `fileEdited` triggers on save, not create
   - Check spelling: `fileEdited` not `fileEdit`

**Common Mistakes:**
- Pattern too specific: `src/components/Button.tsx` (only one file)
- Pattern too broad: `*` (triggers on everything)
- Wrong event type

---

### Unexpected Behavior

**Check:**
1. Instructions are clear and specific
2. No conflicting hooks (disable others temporarily)
3. File patterns aren't too broad

**Debugging:**
- Add logging to shell commands: `echo "Hook triggered" >> /tmp/hook.log`
- Simplify agent prompts to isolate issue
- Test with single file before expanding pattern

---

### Performance Issues

**Solutions:**
1. Limit hook scope with specific file patterns
   - Change `**/*.ts` to `src/**/*.ts`
   - Exclude test files: `!**/*.test.ts`
2. Simplify complex instructions (break into multiple hooks)
3. Ensure shell commands complete quickly (<5 seconds)
4. Reduce trigger frequency (use `agentStop` or `userTriggered` instead of `fileEdited`)

**Performance Checklist:**
- [ ] File patterns are specific (not `*` or `**/*`)
- [ ] Agent prompts are concise (<200 words)
- [ ] Shell commands complete quickly (<5s)
- [ ] Hooks don't trigger on every keystroke
- [ ] Timeout is set appropriately

---

## Examples

### Security Pre-Commit Scanner

**Event:** `agentStop`
**Action:** `askAgent`

```json
{
  "name": "Security Scanner",
  "version": "1",
  "when": {
    "type": "agentStop"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review changed files for potential security issues:\n\n1. Look for API keys, tokens, or credentials\n2. Check for private keys or sensitive credentials\n3. Scan for encryption keys or certificates\n4. Identify authentication tokens or session IDs\n5. Flag passwords or secrets in configuration files\n\nFor each issue found:\n1. Highlight the specific security risk\n2. Suggest a secure alternative\n3. Recommend security best practices"
  }
}
```

---

### Centralized Prompt Logging

**Event:** `promptSubmit`
**Action:** `runCommand`

```json
{
  "name": "Prompt Logger",
  "version": "1",
  "when": {
    "type": "promptSubmit"
  },
  "then": {
    "type": "runCommand",
    "command": "curl -H 'Content-Type: application/json' -XPOST 'http://loghost/loki/api/v1/push' --data-raw '{\"streams\": [{\"stream\": { \"app\": \"kiro\", \"user\": \"'${USER}'\"  }, \"values\": [ [\"'$(date +%s%N)'\", \"'${USER_PROMPT}'\"] ]}]}'"
  }
}
```

**Environment Variables:** `$USER`, `$USER_PROMPT`

---

### i18n Sync Helper

**Event:** `fileEdited`
**Action:** `askAgent`

```json
{
  "name": "i18n Sync",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/locales/en/*.json"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "When an English locale file is updated:\n\n1. Identify which string keys were added or modified\n2. Check all other language files for these keys\n3. For missing keys, add them with a 'NEEDS_TRANSLATION' marker\n4. For modified keys, mark them as 'NEEDS_REVIEW'\n5. Generate a summary of changes needed across all languages"
  }
}
```

---

### Test Coverage Maintainer

**Event:** `fileEdited`
**Action:** `askAgent`

```json
{
  "name": "Test Coverage",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": ["src/**/*.{js,ts,jsx,tsx}", "!src/**/*.test.{js,ts,jsx,tsx}"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "When a source file is modified:\n\n1. Identify new or modified functions and methods\n2. Check if corresponding tests exist and cover the changes\n3. If coverage is missing, generate test cases for the new code\n4. Run the tests to verify they pass\n5. Update coverage reports"
  }
}
```

---

### On-Demand Documentation

**Event:** `userTriggered`
**Action:** `askAgent`

```json
{
  "name": "Generate Docs",
  "version": "1",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Generate comprehensive documentation for the current file:\n\n1. Extract function and class signatures\n2. Document parameters and return types\n3. Provide usage examples based on existing code\n4. Update the README.md with any new exports\n5. Ensure documentation follows project standards"
  }
}
```

---

### Figma Design Validation (MCP)

**Event:** `fileEdited`
**Action:** `askAgent`

```json
{
  "name": "Figma Validator",
  "version": "1",
  "when": {
    "type": "fileEdited",
    "patterns": ["*.css", "*.html"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Use the Figma MCP to analyze the updated html or css files and check that they follow established design patterns in the figma design.\n\nVerify elements like hero sections, feature highlights, navigation elements, colors, and button placements align."
  }
}
```

**Requires:** Figma MCP server configured

---

## Related Tools

- `ReusableTools/validate_json.py` - Generic JSON validator with hook auto-detection
- `ReusableTools/hook_manager.py` - Hook management tool (11 commands)
- `.kiro/hooks/` - Hook files directory

## Usage Guidelines for AI Assistants

### When User Asks About Hooks

1. Reference this file for official AWS documentation
2. Use `validate_json.py` to validate hook JSON syntax
3. Use `hook_manager.py` for hook editing in long sessions (NOT fsWrite)
4. Always verify `version` field is string type

### Creating Hooks for Users

1. Ask about desired trigger (event type)
2. Determine appropriate action type (askAgent vs runCommand)
3. Validate configuration before saving
4. Test with limited scope first

### Editing Hooks in Long Sessions

**CRITICAL:** Use `hook_manager.py` Python tool, NOT fsWrite or file-writer-helper:
```bash
python ReusableTools/hook_manager.py backup <hook_file>
python ReusableTools/hook_manager.py update <hook_file> --field description --value "New description"
```

### Common Pitfalls to Avoid

1. ❌ Using `version: 1` (number) instead of `version: "1"` (string)
2. ❌ Forgetting `when.patterns` for file events
3. ❌ Forgetting `when.toolTypes` for tool events
4. ❌ Using fsWrite for hook editing in long sessions
5. ❌ Overly broad file patterns (`*` instead of `src/**/*.ts`)
6. ❌ Vague agent prompts ("fix the code" instead of specific steps)

---

**Source:** AWS Kiro Documentation (Complete - 7 parts documented 2026-02-23)

**Last Updated:** 2026-02-23