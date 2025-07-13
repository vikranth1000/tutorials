# Coding agents

## Claude code

### Install and configure

- Follow the set-up from https://docs.anthropic.com/en/docs/claude-code/setup

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

### Coding with Claude code

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

### Must read refs
  - https://www.anthropic.com/claude-code
  - https://www.anthropic.com/engineering/claude-code-best-practices
  - https://news.ycombinator.com/item?id=43735550

// https://github.com/anthropics/anthropic-cookbook
// https://github.com/anthropics/courses
// https://www.anthropic.com/claude-code
// https://docs.anthropic.com/en/docs/claude-code/tutorials
// https://news.ycombinator.com/item?id=43735550

# OpenAI Codex
./notes/cs.openai.txt

# Aider

// ./notes/IN_PROGRESS.cs.aider.txt
// ~~https://aider.chat/~~
// [~~https://github.com/Aider-AI/aider~~](https://github.com/Aider-AI/aider)
// ~~Free~~
// # **Aider**
// 
// ## **Installing**
// 
// \> pip install aider-chat
// 
// In case of Unable to list files in git repo: \[Errno 24\] Too many open files
// \> ulimit \-n 8192
// 
// \> aider \--model sonnet \--api-key anthropic=$ANTHROPIC\_KEY
// 
// [https://aider.chat/docs/faq.html\#can-i-use-aider-in-a-large-mono-repo](https://aider.chat/docs/faq.html#can-i-use-aider-in-a-large-mono-repo)
// 
// Tie the output to a markdown
// \> aider \--model sonnet \--api-key anthropic=$ANTHROPIC\_KEY \--chat-history-file aider\_chat.md

# Google CLI

// https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/

# EDAs

- The goal of this guide is to inspire users to be more productive using AI
  tools, successfully accomplish initial set-up. For detailed documentation
  follow the suggested links.

## GitHub Copilot

### Confirm you have access to a license

1. Visit https://github.com/settings/copilot
2. The page should read that **GitHub Copilot Business is active for your
   account**
   - If not, contact the Infra team / GP

### VSCode set-up

1. Open a new VSCode window and open the extensions marketplace with
   `CMD + Shift + X`
2. Install 2 extensions
   - GitHub Copilot
   - GitHub Copilot Chat
3. VSCode might prompt you to sign in using your GH account via a notification
   window in the bottom right, unless you are already signed in
   - You can also sign in by clicking the "Accounts" button in the bottom left
     of the window

- Reference document: https://code.visualstudio.com/docs/copilot/setup

- After successfully logging in, Copilot should automatically start suggesting
  code
  - If it doesn't visit the troubleshooting page
    https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-common-issues-with-github-copilot

### Copilot Code suggestions

- Reference document:
  https://docs.github.com/en/copilot/using-github-copilot/getting-code-suggestions-in-your-ide-with-github-copilot

- The following steps will provide an example for resolution of issue
  https://github.com/cryptokaizen/cmamp/issues/9451 using GitHub Copilot
- In this GH issue we want to add tests for the function
  `datapull/common/universe/universe.py::get_vendor_universe_as_asset_ids`
- Go to the file `datapull/common/universe/test/test_universe.py`
  - If there is a test called `Test_get_vendor_universe_as_assert_ids` you can
    delete it for this example

- For example, suppose we want to add new test cases, typing
  `class Test_get_vendor_universe_as_assert_ids(` and Copilot suggests code
  <img src="figs/improve_productivity_using_ai/image1.png" style="" />

- We can use the mouse to control the generated code or use
  - `TAB` accepts the suggestion
  - `Control + →` will accept only the next word (useful if the suggested code
    is only "kind-of" correct)
  - `Alt + [` / `Alt + ]` show previous / next suggestion, since usually Copilot
    generates multiple ones
  - For a full list of shortcuts refer to the reference docs in the note above

- It is also possible to describe a test in natural language
  <img src="figs/improve_productivity_using_ai/image2.png" style="" />

### Copilot Chat

- Reference document:
  https://docs.github.com/en/copilot/using-github-copilot/asking-github-copilot-questions-in-your-ide

1. You can access the chat in the activity bar on the left
   - If you don't see the icon, right-click on the activity bar and enable
     "Chat"

2. Apart from the general ChatGPT like capabilities, Copilot chat offers unique
   features related to coding
   - **Chat participants**
     - `@workspace` has context about the code in the current workspace, this
       helps Copilot consider the project structure
     - You can also specify "this file" when engineering a prompt for the tab
       you have opened
   - **Chat context**
     - You can use so-called chat variables to include more context; a chat
       variable is accessed via `#`,
       - `#file` adds additional context from a given file
         - E.g. `#file:datapull/common/data/universe.py`
   - **Slash commands**
     - Provide shortcuts to commonly used features
       - E.g. `/tests` to generate unit tests for the selected code

3. For a quick suggestion, you can use inline chat using current line or a
   selection and `CMD + i`
   <img src="figs/improve_productivity_using_ai/image3.png" style="" />
   <img src="figs/improve_productivity_using_ai/image4.png" style="" />

4. Right clicking in a window or on a selection `Copilot` offers quick actions
   of Copilot similar to slash commands, such as:
   - `Explain this`
   - `Fix this`
   - `Generate docs`
   - `Generate tests`

### Tips & Tricks

- The entry point of the GitHub copilot documentation is
  https://docs.github.com/en/copilot
- Tips on prompt engineering:
  https://docs.github.com/en/copilot/using-github-copilot/prompt-engineering-for-github-copilot
- Example prompts:
  https://docs.github.com/en/copilot/using-github-copilot/example-use-cases/example-prompts-for-copilot-chat

- For detailed documentation of integrating VSCode and Copilot:
  https://code.visualstudio.com/docs/copilot/overview

## ChatGPT

## Cursor

## Devin

./docs/code_guidelines/all.improve_productivity_using_ai.how_to_guide.md

https://simonwillison.net/2025/Apr/16/

https://simonwillison.net/series/using-llms/
https://simonwillison.net/series/llms-annual-review/

// New tools to try
// Try refact.ai** Try [https://refact.ai/](https://refact.ai/) $10

// ## Devin

// ## Codeium

// ## Rope
// Experiment with Rope to refactor Python code
// [https://rope.readthedocs.io/en/latest/index.html](https://rope.readthedocs.io/en/latest/index.html)

// Our tools
// llm_transform.py: a tool we have developed that process files through a prompt and / or with vim
// llm_apply_cfile.py
