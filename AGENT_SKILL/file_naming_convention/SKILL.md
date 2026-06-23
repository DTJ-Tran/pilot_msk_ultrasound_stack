# Skill: file_naming_convention

## Trigger Conditions
Any file or directory create, rename, or move operation.

## Rules

### 1. File and Directory Naming
- All files and directories must use `snake_case` (lowercase letters, digits, underscores only).
- No spaces or special characters (except hyphens in specific cases).
- Severity: `[ERROR]`

### 2. Hyphen Usage Exception
- Hyphens (`-`) are allowed ONLY in the following specific filenames (where changing the name would break standard tooling):
  - `docker-compose.yaml`, `docker-compose.yml`
  - `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- Files beginning with '.' (like `.gitignore`, `.env`, `.npmrc`) are exempt from snake_case requirements for the prefix portion, but the suffix should follow naming conventions where practical.
- Any other use of hyphens in file or directory names is prohibited.
- Severity: `[ERROR]`

### 3. Uppercase Reserved for Root Constants
- `UPPER_SNAKE_CASE` is reserved only for root-level configuration constants (e.g., `CONFIG.json`, `Dockerfile`).
- Using `UPPER_SNAKE_CASE` for regular files or directories is prohibited.
- Severity: `[ERROR]`

### 4. Forbidden Extensions
The following file extensions are forbidden in the repository (must be stored externally and referenced by URL):
- `.pdf`, `.pptx`, `.docx`, `.xlsx`, `.csv`, `.zip`, `.pth`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.mp4`, `.mov`, `.avi`, `.dcm`, `.nii`, `.nii.gz`
- Severity: `[ERROR]`

### 5. LEGACY/ Directory Policy
- The `LEGACY/` directory is read-only.
- Any modification to files under `LEGACY/` must include an inline comment `# LEGACY:` explaining why the change is necessary.
- Failure to include this comment when modifying LEGACY/ files is a violation.
- Severity: `[ERROR]`

### 6. Test File Naming
- Test files must mirror the source file path in a parallel `tests/` directory.
- Example: `src/module.py` → `tests/test_module.py`
- Severity: `[WARN]`