
---
name: code-review
description: Reviews existing code for bugs, security vulnerabilities, logic errors, maintainability issues, and violations of project conventions. Use when reviewing code changes, inspecting pull requests, or checking implementation quality. Do not automatically modify code during a review.
---

# Code Review

## Objective

Review code carefully and identify problems before they reach the application.

## Workflow

### 1. Understand the context
- Inspect the relevant files before reviewing.
- Read the project's AGENTS.md instructions.
- Understand what the code is supposed to accomplish.
- Check related functions, models, views, and tests when relevant.

### 2. Inspect the implementation
Look for:

- Incorrect business logic.
- Potential bugs and edge cases.
- Security vulnerabilities.
- Poor error handling.
- Unnecessary code duplication.
- Performance problems.
- Violations of Django best practices.
- Missing or inadequate tests.

### 3. Verify findings
- Trace the relevant code before reporting an issue.
- Do not report speculative problems as confirmed bugs.
- Run relevant existing tests when appropriate.
- Never claim that a test passed unless it was actually executed.

### 4. Report findings

Present findings in this order:

1. Critical issues
2. High-priority issues
3. Medium-priority issues
4. Low-priority suggestions

For each finding, include:
- File and relevant line number.
- What the problem is.
- Why it matters.
- A suggested solution.

### 5. Final summary

Provide:
- Overall review result.
- Confirmed issues.
- Tests executed and their results.
- Suggestions for improvement.

## Important Rules

- Do not modify files during a review unless explicitly asked.
- Do not rewrite working code without a clear reason.
- Prefer specific, evidence-based findings.
- Follow existing project conventions.
- Explain important architectural concerns clearly.
