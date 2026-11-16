
---
name: django-debugging
description: Investigates and debugs Django application errors, unexpected behavior, failed requests, authentication problems, database issues, and failing tests. Use when diagnosing bugs, tracing errors, or finding root causes in Django projects.
---

# Django Debugging

## Objective

Investigate Django application problems systematically, identify their root causes, and implement verified fixes when authorized.

## Workflow

### 1. Understand the problem
- Ask what behavior was expected.
- Identify what actually happened.
- Inspect the error message, traceback, or browser console.
- Identify the affected feature.

### 2. Investigate before changing code
- Inspect relevant files.
- Trace the execution flow.
- Check URLs, views, models, templates, and JavaScript where relevant.
- Inspect related settings and configurations.
- Check recent changes if Git history is available.

### 3. Identify the root cause
- Distinguish the actual cause from symptoms.
- Consider possible causes before selecting one.
- Use logs, tracebacks, and tests as evidence.
- Avoid guessing or making random changes.

### 4. Explain the diagnosis

Before implementing a fix, explain:

- What caused the problem.
- Which part of the application is affected.
- Why the problem occurred.
- What change would solve it.

### 5. Implement the fix
- Make the smallest appropriate change.
- Follow Django best practices.
- Preserve existing working functionality.
- Avoid unnecessary dependencies.
- Do not rewrite unrelated code.

Only modify files when the user has authorized implementation.

### 6. Verify the fix
- Run relevant tests.
- Check related functionality.
- Inspect the final changes.
- Report any remaining errors.
- Never claim successful verification without evidence.

## Important Rules

- Investigate before modifying files.
- Never hide errors just to make the application appear functional.
- Do not assume the first error message reveals the root cause.
- Preserve existing project architecture.
- Explain important technical decisions.
- If the root cause is uncertain, communicate that uncertainty.
