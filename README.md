# Pilot Project - MSK Ultrasound Stack

## File Type Guidelines
- Only include text‑based files that can be viewed and edited directly in an IDE: Markdown (`.md`), HTML (`.html/.htm`), source code files (`.py`, `.java`, `.js`, `.ts`, `.cpp`, `.h`, etc.), configuration files (`.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.cfg`), and plain text (`.txt`).
- Do **not** commit binary or non‑text‑friendly files such as PDFs, PowerPoint presentations (`.pptx`), Word documents, Excel spreadsheets (`.csv`, `.xlsx`), ZIP archives, or compiled binaries.
- For large datasets, documents, presentations, or binary assets, store them in an external storage system (e.g., Amazon S3, Google Cloud Storage, Azure Blob) and reference them via a URL/link in the appropriate markdown or documentation file.
- Images that illustrate documentation or design (e.g., diagrams, screenshots) may be committed directly **if** they are small and aid understanding, but large image datasets must be stored externally and linked.
- Keep the repository lightweight and IDE‑friendly to ensure fast cloning, searching, and navigation.
- Use **snake_case** naming for files and directories (lowercase letters, numbers, and underscores only). Avoid spaces and special characters. Hyphens are discouraged except for specific configuration files like `docker-compose.yaml` or `docker-compose.yml`. Uppercase is acceptable for constants (e.g., `CONFIG.json`) but prefer lowercase.

## Overview
This repository contains the research, design, and implementation materials for the MSK Ultrasound Stack pilot project. It includes documentation, design artifacts, source code, and supporting files organized to facilitate collaborative development while maintaining clear separation between shared assets and individual developer secrets.

## Directory Structure
```
PILOT_PROJECT/
├── .gitignore                # Git ignore rules (includes OS/editor temp files, dependencies, and `secrets/` folder)
├── Reading_docs/             # Reference and background materials
│   ├── PLAN/                 # Project plans and timelines
│   ├── Requirement_Analysis/ # Stakeholder and functional requirements
│   ├── Technical_Brainstorming/ # Brainstorming notes, sketches, whitepapers
│   └── User_Analysis/        # User personas, workflows, and usability research
├── workspace/                # Primary working area for sprints and development
│   ├── sprint_1_2/           # Example sprint folder
│   │   ├── CAVEAT_TASK.md    # Known limitations and caveats
│   │   ├── CONTEXT.md        # Sprint context and goals
│   │   ├── DESIGN_MATERIAL/  # UI/UX mockups, wireframes, style guides
│   │   ├── docs/             # Generated or supplemental documentation
│   │   ├── PROJECT_VIS.md    # Project visualization and architecture diagrams
│   │   ├── SOFTWARE_SYSTEM_DESIGN_FR_25.md # Detailed software design specification
│   │   ├── SOLUTION_ARCHITECTURE_SPEC.md   # Solution architecture overview
│   │   └── visualization/    # Charts, diagrams, and visual assets
│   └── ...                   # Additional sprint folders as needed
├── secrets/                  # **Developer‑managed secrets** (NOT tracked by git)
│   │   # Each developer should maintain their own copy of this folder
│   │   # locally (or in a secure secret manager) and add it to their personal .gitignore.
│   │   # Example contents: API keys, database passwords, TLS certs, etc.
│   │   # The repository .gitignore intentionally ignores this entire directory.
│   └── .gitkeep              # Placeholder to keep the folder in repo structure
└── README.md                 # This file
```

## Getting Started
1. **Clone the repository**  
   ```bash
   git clone git@github.com:DTJ-Tran/pilot_msk_ultrasound_stack.git
   cd pilot_msk_ultrasound_stack
   ```

2. **Set up your local secrets**  
   - Create a `secrets/` directory (if not already present) in your local clone.  
   - Add any required API keys, certificates, or configuration files **here**.  
   - Ensure `secrets/` is listed in your personal `.gitignore` (the repository‑level `.gitignore` already ignores this folder).

3. **Explore the documentation**  
   - Start with `Reading_docs/PLAN/` for project timeline and milestones.  
   - Review `workspace/sprint_1_2/CONTEXT.md` for current sprint goals.  
   - Check `workspace/sprint_1_2/DOCUMENTATION/` for architecture diagrams and design specs.

4. **Set up your development environment**  
   - Follow language‑specific setup guides found in `workspace/sprint_<n>/docs/` (if any).  
   - Install dependencies listed in any `requirements.txt`, `package.json`, `pom.xml`, etc., that appear in sprint folders.

## Codebase Architecture & Style Guide
### High‑Level Architecture
- **Modular Layers**: The system is organized into presentation, application/services, and data access layers (see `SOLUTION_ARCHITECTURE_SPEC.md`).  
- **Interface‑Driven**: Core services communicate via well‑defined interfaces/contracts to enable easy substitution of implementations (e.g., mock services for testing).  
- **Configuration‑Driven**: Environment‑specific settings (endpoints, feature flags) are externalized and should be injected via the `secrets/` folder or environment variables—not hard‑coded.

### Coding Conventions
- **Language‑Specific**: Follow the official style guide for each language used (e.g., PEP 8 for Python, Google Java Style, Airbnb JS/TS, etc.).  
- **Naming**: Use descriptive, intent‑revealing names. Constants in `UPPER_SNAKE_CASE`, classes/functions in `PascalCase`/`camelCase` as appropriate.  
- **Documentation**: Every public class, function, and module must include a docstring/comment describing purpose, parameters, return values, and side‑effects.  
- **Error Handling**: Prefer explicit exceptions over error codes; log meaningful messages at appropriate levels (debug/info/warn/error).  
- **Testing**: Write unit tests for new logic; aim for >80% coverage on critical paths. Keep tests in parallel `test/` directories adjacent to source.  
- **Commits**: Write clear, conventional commit messages (type: scope? subject). Keep commits atomic and focused.

### Dependency Management
- Pin exact versions in lockfiles (`requirements.txt`, `package-lock.json`, `pom.xml`, etc.).  
- Avoid committing compiled binaries or generated documentation—these should be produced locally or in CI.

## Collaboration Guidelines
- **Branch Naming**: Use `feature/<short-description>`, `bugfix/<issue-id>`, or `release/<version>`.  
- **Pull Requests**:  
  - Provide a concise summary of changes.  
  - Link to any related issue or task.  
  - Include screenshots or diagrams when UI/UX is affected.  
  - Request at least one review from a teammate.  
- **Code Review**: Look for correctness, adherence to style, test coverage, and documentation updates.  
- **Issues & Tracking**: Use the linked GitHub Issues board (or your preferred tracker) to log bugs, features, and technical debt.

## Secrets Management (Important)
The `secrets/` directory **must not** be committed to the repository. The repository‑level `.gitignore` already contains:

```
secrets/
```

Each developer is responsible for:
- Creating their own `secrets/` folder locally.  
- Storing sensitive items (API keys, passwords, certificates) there.  
- Referencing these values in code via environment variables or a secure config loader that reads from `secrets/`.  
- Backing up their secrets securely (e.g., using a password manager or encrypted vault).

If you need to share a secret securely with a teammate, use your organization’s approved secret‑sharing tool (e.g., 1Password Teams, HashiCorp Vault, AWS Secrets Manager) — **never** commit plaintext secrets.

## License
[Specify your license here, e.g., MIT, Apache 2.0, or internal proprietary.]

---

*Welcome to the team! If you have questions, reach out to the project lead or consult the `Reading_docs/` for background material.*