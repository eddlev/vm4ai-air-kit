# AIR Update and Rollback

## Update rule

Treat each release as one coherent file set. Do not mix a manifest from one release with modules from another.

1. Record the current release/tag or file hashes.
2. Back up the current `prompts/`, `profiles/`, and `runtime/` directories.
3. Replace the candidate files as one set.
4. Run JSON, sentinel, manifest, and documentation-link validation.
5. Run a boot-plan smoke test.
6. Keep the previous archive until operator acceptance.

## Rollback

Restore the complete prior set, not individual files. Re-run `validate-manifest` and compare the restored prompt hashes with the prior release manifest.

## Handoff compatibility

Preserve the handoff template schema identity. A handoff with newer fields may require inspection or regeneration under the target release.

Repository merge, tag, and release publication remain separate approvals from local candidate validation.
