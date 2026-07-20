# AIR Release Process

## v0.3.0 release profile

The v0.3.0 line introduces the modular runtime and integrated documentation while retaining the monolithic prompt path.

Required release assets:

- `AIR-v0.3.0.zip` — complete user-facing release bundle;
- `AIR-v0.3.0-repository-overlay.zip` — files to add or replace in the public repository;
- `AIR-v0.3.0-SHA256SUMS.txt` — archive checksums;
- `AIR-v0.3.0-RELEASE-MANIFEST.json` — fixed-source and validation evidence;
- release notes matching `release/v0.3.0/RELEASE_NOTES.md`.

## Release gates

1. Select the target version.
2. Pin the repository base commit.
3. Construct and validate the repository overlay.
4. Build the complete release asset and checksums.
5. Run structural, modular-boot, handoff-tool, documentation-link, update, and rollback checks.
6. Obtain explicit repository-mutation approval.
7. Create a review branch and pull request.
8. Review and merge separately.
9. Create the tag and publish release assets only after publication approval.

Repository mutation, merge, tagging, release publication, and public announcement are distinct actions. A valid signature, passing local tool, or approved release identity does not authorize any of them automatically.
