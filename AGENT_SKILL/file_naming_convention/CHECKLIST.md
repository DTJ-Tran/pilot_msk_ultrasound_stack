# Checklist: file_naming_convention

## File/Directory Creation/Rename/Move
- [ ] All new files and directories use `snake_case` (lowercase, digits, underscores only)
- [ ] No spaces or special characters in file/directory names
- [ ] Hyphens (`-`) used only in `docker-compose.yaml`, `docker-compose.yml`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- [ ] `UPPER_SNAKE_CASE` used only for root-level configuration constants (e.g., `CONFIG.json`, `Dockerfile`)
- [ ] Forbidden extensions (`.pdf`, `.pptx`, `.docx`, `.xlsx`, `.csv`, `.zip`, `.pth`, `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.mp4`, `.mov`, `.avi`, `.dcm`, `.nii`, `.nii.gz`) are not present in the repository
- [ ] Any file under `LEGACY/` that is modified includes an inline comment `# LEGACY:` explaining the change
- [ ] Test files follow the pattern: `tests/<same_path_as_source>/test_<source_filename>`

## Verification Steps
1. Check all created/renamed/moved files for snake_case naming
2. Verify hyphen usage is limited to allowed files: docker-compose.yaml/.yml, package-lock.json, yarn.lock, pnpm-lock.yaml
3. Confirm UPPER_SNAKE_CASE appears only for root config files
4. Scan for forbidden file extensions
5. Inspect any changes in LEGACY/ directory for required comment
6. Validate test file placement matches source file structure