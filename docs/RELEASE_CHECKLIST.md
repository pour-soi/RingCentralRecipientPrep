# PourSend Release Checklist

Use this checklist for future PourSend Windows releases. It is a release-process guide only; do not change historical releases unless a separate maintenance task explicitly requires it.

## 1. Release Audit

- Confirm the current branch is `main`.
- Confirm `git status --short` is clean before starting.
- Confirm local `main` matches `origin/main`.
- Confirm the target tag does not already exist locally or on GitHub.
- Confirm no GitHub Release already exists for the target tag.
- Review the previous release page and asset names.

## 2. Version Update

- Update the application version constant.
- Update user-facing current-version references in the README.
- Update build or packaging metadata only where the current version is intentionally stored.
- Update tests that verify the current version.
- Do not rewrite old changelog or release-history entries.

## 3. Local Verification

Run:

```powershell
python -m unittest
python -m compileall main.py app core tests
git diff --check
```

Also confirm:

- The About dialog displays the new version.
- Active current-version references use the new version.
- Historical references to older releases remain unchanged.
- No recipient-management behavior, storage format, import/export behavior, or UI workflow changed unless the release explicitly requires it.

## 4. Windows UI Smoke Test

On Windows, verify:

- The app launches from source.
- The app launches from an extracted release package.
- Logo, window icon, taskbar icon, and About dialog branding render correctly.
- The interface remains usable at 100%, 125%, and 150% display scaling.
- Adding a recipient, restarting, searching, copying, and grouping still work.
- Data persists in the expected local data folder.

## 5. Commit And Push

- Create one version-bump commit with a clear message.
- Push `main` to `origin/main`.
- Confirm local `main` and `origin/main` point to the same commit.

## 6. Build Artifact

- Run the `Build PourSend Windows executable` workflow from the release commit.
- Confirm the workflow uses the expected commit.
- Confirm tests and syntax checks pass in GitHub Actions.
- Confirm the package name matches the application version, for example `PourSend-vX.Y.Z-Windows.zip`.
- Confirm the ZIP contains `PourSend.exe`, `README.md`, and `LICENSE`.
- Confirm the SHA-256 checksum file is generated.
- Download the generated artifact and inspect it before publishing the release.

## 7. Tag

- Create an annotated tag on the exact release commit.
- Use the release version as the tag name, for example `vX.Y.Z`.
- Push the tag to origin.
- Confirm the tag commit matches the release commit.

## 8. GitHub Release

- Create the GitHub Release from the pushed tag.
- Use a clear release title.
- Attach the newly generated Windows ZIP artifact.
- Attach or publish the SHA-256 checksum.
- Do not reuse artifacts from earlier commits.
- Do not mark the release as a draft or prerelease after final verification passes.

## 9. Final Verification

- Re-download the published ZIP from the Release page.
- Extract it into a normal Windows folder.
- Run `PourSend.exe`.
- Confirm the app version, branding, icons, data persistence, copy, search, and grouping behavior.
- Confirm `git status --short` is clean after release work.
- Record the release URL, tag, commit hash, ZIP filename, workflow result, and any warnings.

## Code Signing

PourSend is currently distributed as an unsigned portable executable. Code signing requires a valid Windows code-signing certificate and a separate signing step. Do not fake signing, reuse unrelated certificates, or claim a binary is signed unless the signature is verified.
