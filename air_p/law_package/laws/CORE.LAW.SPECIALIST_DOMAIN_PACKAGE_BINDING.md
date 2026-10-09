==================================================
SPECIALIST DOMAIN PACKAGE BINDING LAW
==================================================

Patch marker: AIR_SPECIALIST_PACKAGE_BINDING_V2

Binding is explicit and scoped.

Required sequence:
1. ATTACHED or DISCOVERED
2. CLASSIFIED
3. PACKAGE_INTEGRITY_CHECKED
4. COMPATIBILITY_REVIEWED
5. SELECTED
6. USER_APPROVED_FOR_BINDING, USER_APPROVED_FOR_BINDING_BY_RESPONSIVE_ACTION, or HANDOFF_RESTORED_APPROVAL
7. BOUND

Automatic binding from filename, task similarity, or package presence is prohibited. `USER_APPROVED_FOR_BINDING_BY_RESPONSIVE_ACTION` is not automatic binding; it is explicit approval produced by a pre-disclosed exact user response under AIR_RESPONSIVE_BINDING_APPROVAL_M1.

Binding record must include:
- component designations and versions
- package manifest identity when applicable
- exact approved scope
- authorized effects
- excluded effects
- conflicts and precedence
- required evidence
- stop conditions
- approval source

A component may be used as unbound reference material without becoming an operator. The active contract and Core runtime govern conflicts.

