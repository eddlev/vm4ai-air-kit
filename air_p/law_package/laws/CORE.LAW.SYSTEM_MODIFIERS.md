==================================================
AIR SYSTEM MODIFIER LAW
==================================================

Patch marker: AIR_MINIMAL_SYSTEM_MODIFIERS_V2

The CLI-like layer contains only these canonical AIR system modifiers:
- air -o on
- air -o -min
- air -t on
- air -t off

Command parsing is case-insensitive and tolerant of repeated whitespace.

Modifier families are independent:
- `-o` controls AIR object visibility only
- `-t` controls evidence presentation and packaging only; it never changes evidence obligations or preservation

Unknown `air` switches:
- state that the switch is unsupported
- show only the four canonical switches and their meanings
- do not invent behavior

Temporary v1 compatibility aliases:
- air object on -> air -o on
- air compact -> air -o -min
- air object off -> air -o -min, with an explanation that required objects cannot be disabled

Test-evidence modifier behavior:
- `air -t on` selects EXPANDED_EVIDENCE_PRESENTATION for subsequent evidence displays/packages
- `air -t off` selects STANDARD_EVIDENCE_PRESENTATION and is the default presentation mode
- changing `-t` does not retroactively alter a completed run

All other AIR functions are requested in normal human language. Examples:
- What are we doing now?
- What is blocking this?
- Show the evidence.
- Is this ready?
- Make a handoff.

System modifiers never bypass AIR_GATE, evidence, active scope, approval, safety, or required object emission.

