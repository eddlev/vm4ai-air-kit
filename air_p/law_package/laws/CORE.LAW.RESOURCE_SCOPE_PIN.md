==================================================
RESOURCE SCOPE PIN LAW
==================================================

Patch marker: AIR_RESOURCE_SCOPE_PIN_V2

When an active step may use tools or mutate files, repositories, systems, or external state, AIR_ARTIFACT must contain resource_scope_pin.

resource_scope_pin minimum fields:
- pin_id
- repositories
- branches
- paths_or_resource_ids
- external_systems
- environments
- credential_or_permission_classes
- allowed_action_classes
- canonicalization_and_match_rule
- scope_expansion_rule
- pin_validation_state

Discovering, listing, reading, or mentioning another resource does not add it to scope. Similar names, account ownership, nearby repositories, parent folders, related projects, or prior context do not authorize action.

Any target outside the pin routes to REVIEW, RESCOPE_REQUIRED, or REJECT before tool execution. Scope expansion requires a visible artifact revision and the approval required by the active contract.

