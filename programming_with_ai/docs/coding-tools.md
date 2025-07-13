# Coding agents

## Claude code

- Refs
  - https://www.anthropic.com/claude-code
  - https://www.anthropic.com/engineering/claude-code-best-practices
  - https://news.ycombinator.com/item?id=43735550

### Install and configure

Follow https://docs.anthropic.com/en/docs/claude-code/setup

### 

## What is Claude Code?
- Specialized capability of Claude for software development tasks.
- Designed to help with:
  - Writing code from scratch.
  - Debugging existing code.
  - Explaining code logic.
  - Converting code between languages.
  - Generating tests and documentation.

## Core Use Cases
- **Explain**
  - Break down code line-by-line.
  - Clarify complex algorithms.
- **Write**
  - Generate functions, classes, modules.
  - Follow user style guides and constraints.
- **Transform**
  - Refactor code for readability or performance.
  - Convert code to different frameworks/languages.
- **Complete**
  - Fill in partial implementations.
  - Suggest alternative solutions.
- **Test**
  - Generate unit tests.
  - Identify edge cases.

## Strengths
- Handles long code files and complex projects.
- Maintains conversational context for iterative coding.
- Produces clear, well-commented code.
- Supports multiple programming languages.

## How It Works
- Uses context window to “read” entire files if needed.
- Retains history to apply consistent style/logic.
- Can work with multiple files at once.

## Best Practices
- Provide clear instructions:
  - Define programming language.
  - Specify libraries, versions, frameworks.
  - Share input/output expectations.
- Break requests into steps for complex tasks.
- Ask for explanations alongside generated code to verify intent.

## Limitations
- May produce non-compiling code — always test.
- Can hallucinate libraries or functions — verify usage.
- May require iterative refinement for large systems.

## Example Prompt
> “Write a Python function that parses a CSV file and returns a dictionary keyed by column names. Include type hints and docstrings.”

## OpenAI Codex
./notes/cs.openai.txt

## Aider

./notes/IN_PROGRESS.cs.aider.txt

## Google CLI
https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/

# EDAs

ChatGPT
Cursor

# To reorg
Devin

./docs/code_guidelines/all.improve_productivity_using_ai.how_to_guide.md

https://simonwillison.net/2025/Apr/16/

https://simonwillison.net/series/using-llms/
https://simonwillison.net/series/llms-annual-review/

https://github.com/anthropics/anthropic-cookbook

https://github.com/anthropics/courses

# **New tools to try**

### **ISSUE: Try refact.ai**

Try [https://refact.ai/](https://refact.ai/)
$10

### **~~ISSUE: Try Aider~~**

~~https://aider.chat/~~
[~~https://github.com/Aider-AI/aider~~](https://github.com/Aider-AI/aider)
~~Free~~

### **ISSUE: Devin**

### **ISSUE: Claude code**

// https://www.anthropic.com/engineering/claude-code-best-practices

- Claude Code
  - Command line for agentic coding
  - Provides model access without forcing workflows

- Automatically pulls context into prompts

### 1. Customize your setup

- `CLAUDE.md` is pulled in at the beginning of each context
  - Code style guidelines
  - Testing instructions
  - Repo etiquette
  - Dev env set up

- It can be in each dir of the repo and in your home folder

- Tune your `CLAUDE.md`
  - Use instructions, e.g., `IMPORTANT` and `YOU MUST`

### 2. Give Claude more tools

- Curate list of allowed tools
  - `.claude/settings.json`

- Give Claude more tools
  - Knows MCP and REST APIs
  - Knows GitHub `gh` and Unix tools
  - Give your tools name and usage examples
  - Document used tools in `CLAUDE.md`

- Store prompt templates in Markdown files in `.claude/commands`
  - Become available as `/` commands (you can pass commands)

### 3. Try common workflows

- Ask to read relevant files (but tell it not to write any code)
  - E.g., `read logging.py`
- Ask to make a plan for how to approach a specific problem
  - Use the word `think` < `think hard` < `ultrathink` to allocate thinking
    budget
  - Create a doc (or GH issue) with its plan
- Ask to implement solution in code
  - Ask to verify how reasonable is the solution or pieces
- Ask to commit and create a PR
  - Ask to update READMEs and changelog

- Test-driven development (TDD) becomes powerful with agentic coding
- Ask to write tests based on expected input / output pairs
  - Be explicit asking to avoid creating mock implementations for functionalities
    that don't exist yet
- Tell to run the tests and confirm they fail
  - Often helpful to tell not to write implementation
- Ask to commit tests when satisfied with them
- Ask to write code that passes the tests, without modifying the tests
  - Tell to keep going until all tests pass
- Ask to commit code when satisfied

- Codebase Q&A
  - Use for learning and exploration
  - Ask questions like in pair programming

- Use to interact with Git
- Use to interact with GitHub
  - Create PRs
  - Fix failing builds or linter warnings

- Read and write Jupyter notebooks
  - Have CC and .ipynb opened in VS code
  - Make data "aesthetically pleasing"

### 4. Optimize your workflow

- Be specific and give clear directions to avoid iterations
  - Bad: Add tests for `foo.py`
  - Good: write a new test case for `foo.py`, covering edge case where ..., avoid
    mocks

- Use images when working with design mocks for UI and visual charts for analysis

- Give URLs to fetch and read

- You can get better results by being an active collaborator and guiding
  - Explain the task thoroughly
  - Course correct

  - Ask to make a plan
  - Press escape to interrupt
  - Double-escape to jump back in history and edit a previous prompt
  - Ask to undo changes

- Use /clear to keep context focused during long sessions

- Use a checklists for complex workflows
  - E.g., when fixing lint errors, tell to run the lint command, write all
    resulting errors to a md checklist
  - Instruct to address each issue one by one, fixing and verifying before
    checking it off and moving to the next one

### 5. Use headless mode to automate infra

- Use `-p` flag to interact with CI, pre-commit hooks, automation scripts
  - E.g., triage a new issue created in a repo
- Use as a linter
  - Identify typos, stale comments, misleading function or var names

### 6. Multi-Claude workflows

- It is better to have a single instance handle everything
  - Have one C write code, another C verify it
  - Use C to write code
  - Start a second C in another terminal
  - Have a second C review the first C's work
- Create multiple checkouts of your repo
- Use git worktrees

// https://www.anthropic.com/claude-code
// https://docs.anthropic.com/en/docs/claude-code/tutorials

// https://news.ycombinator.com/item?id=43735550

### **ISSUE: Try Codeium**

### **Experiment with Rope to refactor Python code**

[https://rope.readthedocs.io/en/latest/index.html](https://rope.readthedocs.io/en/latest/index.html)

# **Aider**

## **Installing**

\> pip install aider-chat

In case of Unable to list files in git repo: \[Errno 24\] Too many open files
\> ulimit \-n 8192

\> aider \--model sonnet \--api-key anthropic=$ANTHROPIC\_KEY

[https://aider.chat/docs/faq.html\#can-i-use-aider-in-a-large-mono-repo](https://aider.chat/docs/faq.html#can-i-use-aider-in-a-large-mono-repo)

Tie the output to a markdown
\> aider \--model sonnet \--api-key anthropic=$ANTHROPIC\_KEY \--chat-history-file aider\_chat.md


Tools
Cursor
Free?
Causify can get a license
Cursor: it's a porting of VS code + Copilot, with better AI - human integration
Our tools
llm_transform.py: a tool we have developed that process files through a prompt and / or with vim
llm_apply_cfile.py
Aider
Free:
https://aider.chat/
https://github.com/Aider-AI/aider

