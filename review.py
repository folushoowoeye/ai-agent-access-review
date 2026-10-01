import json
from datetime import date

with open("agents.json", encoding="utf-8") as file:
    agents = json.load(file)

with open("policy.json", encoding="utf-8") as file:
    policies = json.load(file)

for agent in agents:
    agent_id = agent["agent_id"]
    policy = policies.get(agent_id)

    print(f"\nReviewing: {agent_id}")
    owner = agent.get("owner")

    if not isinstance(owner, str) or not owner.strip():
        print("FINDING: No accountable owner recorded.")
    else:
         print(f"Owner recorded: {owner}")


    if policy is None or "approved_permissions" not in policy:
        print("NEEDS REVIEW: Approved permissions are missing.")
        continue

    if "permissions" not in agent:
        print("NEEDS REVIEW: Actual permissions are missing.")
        continue

    expiry_text = policy.get("approval_expires")

    if not isinstance(expiry_text, str) or not expiry_text.strip():
        print("NEEDS REVIEW: Approval expiry date is missing.")
    else:
        try:
            expiry_date = date.fromisoformat(expiry_text)
        except ValueError:
            print("NEEDS REVIEW: Approval expiry date is invalid.")
        else:
            if expiry_date < date.today():
                print(f"FINDING: Access approval expired on {expiry_date}.")
            else:
                print(f"Approval valid through: {expiry_date}")
        actual_permissions = agent.get("permissions")
    approved_permissions = policy.get("approved_permissions")

    permission_lists = [actual_permissions, approved_permissions]

    if not all(
        isinstance(items, list)
        and all(isinstance(item, str) and item.strip() for item in items)
        for items in permission_lists
    ):
        print("NEEDS REVIEW: Permissions must be lists of non-empty text values.")
        print("SKIPPED: Human approval check requires valid permission records.")
        continue

    actual = set(actual_permissions)
    approved = set(approved_permissions)
    extra_permissions = actual - approved

    if extra_permissions:
        print("FINDING: Permissions exceed approved access.")
        for permission in sorted(extra_permissions):
            print(f"  Remove or seek approval for: {permission}")
    else:
        print("PASS: No permissions exceed approved access.")

    required_approval = policy.get("human_approval_required_for")
    enabled_approval = agent.get("human_approval_enabled_for")
    approval_lists = [required_approval, enabled_approval]

    if not all(
        isinstance(items, list)
        and all(isinstance(item, str) and item.strip() for item in items)
        for items in approval_lists
    ):
        print("NEEDS REVIEW: Human approval records must be lists of non-empty text values.")
    else:
        required_for_current_access = set(required_approval) & actual
        missing_controls = required_for_current_access - set(enabled_approval)

        if missing_controls:
            for permission in sorted(missing_controls):
                print(f"FINDING: Human approval missing for: {permission}")
        else:
            print("PASS: No required human approval controls are missing.")