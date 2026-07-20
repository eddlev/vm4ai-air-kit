# Recovering an AIR Workstream After a Tool-Runtime Outage

## Incident

During the authorized WS7 schema-consistency repair, local code-execution calls failed before execution. File retrieval remained available. No partial mutation occurred.

## Correct response

AIR failed closed:

1. preserved the prior approval and exact repair scope;
2. distinguished file availability from execution availability;
3. did not claim mutation, hashing, repackaging, or validation;
4. generated a handoff carrying sources, hashes, blockers, and the next gate;
5. required a fresh-session source-confirmation checkpoint;
6. resumed from the interrupted repair rather than redesigning WS7;
7. kept WS8, repository mutation, publication, and release blocked.

## Lessons

- Authorization can survive a session failure, but source identity must be re-established.
- A tool outage is not evidence that source files were corrupted or lost.
- A generated handoff is not cryptographic proof unless locally verified.
- No command execution means no mutation evidence.
- Recovery should preserve the current in-progress gate, not jump to the next workstream.

The repair later completed with executed validation and explicit WS7 approval. This case demonstrates continuity discipline, not uninterrupted backend availability.
