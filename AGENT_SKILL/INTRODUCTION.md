# VKIST MSK Pilot — Shared Agent Enforcement Skills

## Goal
Create up to 5 shareable agent skills under `PILOT_PROJECT/AGENT_SKILL/` that automatically guide coding agents (Claude Code, Gemini CLI, KILO) to follow project conventions from `README.md` and architecture specs.

## How to add a new skill?
1. Create a new folder under AGENT_SKILL/<skill_name>/
2. Add SKILL.md, EXAMPLES.md, CHECKLIST.md
3. Update this INTRODUCTION.md index
4. Open a PR with at least one EXAMPLES.md entry per rule

## Skills Index
| Skill | Covers |
|-------|--------|
| file_naming_convention | File/dir names, forbidden extensions, LEGACY/ policy |
| coding_convention | Python PEP8, TS Airbnb, docstrings, error handling, RBAC |
| interface_contract_hygiene | Contract files, versioning, breaking-change policy |
| secrets_and_phi_safety | Secrets loading, PHI exclusion, CI safety, gitignore |
| design_pattern_compliance | Layered arch, DI, Zustand, Terraform IaC, pinning |