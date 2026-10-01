\# AI Agent Access Review: Findings



\## Scope



This project reviews fictional AI agent records against a separate access policy. It checks for excessive permissions, missing ownership, expired approvals and missing human approval controls.



The review examines supplied configuration records. It does not connect to live systems or enforce access restrictions.



\## Current findings



\### Support assistant: expired access approval



\*\*Evidence:\*\* The policy records an approval expiry date of 30 September 2026. The checker flagged it as expired when the review ran.



\*\*Implication:\*\* The recorded approval is no longer current. This does not establish whether the access is still needed.



\*\*Recommended action:\*\* The Customer Support Team should confirm the agent’s business need and seek a fresh access review. Update the expiry date only after approval is granted. Remove access that is no longer required.



\*\*Responsible owner:\*\* Customer Support Team.



\*\*Status:\*\* Open.



\### Invoice assistant: no findings in the checks performed



Its recorded permissions match the policy. An owner is recorded, and the approval expiry date was still valid when the review ran.



The record now lists human approval as enabled for payment execution, matching the policy requirement.



This result does not verify that a live payment system actually enforces human approval.



\## Remediation demonstrated



During testing, the support assistant had an unapproved permission to delete tickets. Removing that permission resolved the excessive-access finding.



The invoice assistant initially lacked a recorded human approval control for payment execution. Adding the control to its fictional record resolved that finding.



These changes demonstrate detection and rechecking within sample data, not changes to a live system.



\## Validation



Eight automated tests cover compliant access, excessive permissions, blank ownership, expired approval, invalid expiry dates, missing human approval controls and selected missing records.



All eight test cases reported `ok` in the observed run.



\## Limitations



Results depend on the accuracy of the supplied records and the computer’s date. A recorded owner does not prove that the team has accepted responsibility.



A passing check is limited to the rule assessed. It is not a security certification or a complete assessment of an AI agent’s safety.

