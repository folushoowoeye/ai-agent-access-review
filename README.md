\# AI Agent Access Review Checker



A Python prototype that compares fictional AI agent access records against an approved policy and reports issues requiring attention.



For example, an assistant approved to read support tickets and draft replies should not have permission to delete tickets.



\## What it checks



| Check | What it identifies |

|---|---|

| Permissions | Granted permissions that exceed approved access |

| Ownership | A missing or blank accountable owner |

| Approval expiry | Access approval that has expired |

| Human approval | Granted actions missing a required approval control |



Selected missing or invalid records produce `NEEDS REVIEW` rather than a pass. When permission data is invalid, the dependent human approval check is skipped.



\## Project files



\- `agents.json`: fictional agent records and current access.

\- `policy.json`: approved permissions and approval requirements.

\- `review.py`: the access checker.

\- `test\_review.py`: eight automated tests.

\- `findings.txt`: captured checker output.

\- `findings.md`: findings, recommended actions and limitations.



\## Requirements



Python 3.10 or later. Developed and tested with Python 3.13.9 on Windows using Anaconda Prompt.



Only Python’s standard library is used. No extra packages are required.



\## Run the checker



Open a terminal in the project folder:



```text

python review.py

```



Save the output to a report:



```text

python review.py > findings.txt

```



Run the automated tests:



```text

python -m unittest -v

```



\## Understanding the results



\- `FINDING`: a review rule identified an issue.

\- `NEEDS REVIEW`: evidence is missing or invalid.

\- `PASS`: the specific check found no issue.

\- `SKIPPED`: a dependent check could not run.



An agent can pass one check while failing another. There is no overall compliance verdict.



Approval remains valid throughout its expiry date. Results use the computer’s current date, so expiry findings can change over time.



\## Example findings and remediation



During development, the checker detected an unapproved `tickets:delete` permission. Removing it resolved that finding.



It also detected a missing human approval control for `payments:execute`. Updating the fictional agent record to include that control resolved the finding.



The support assistant’s expired approval remains an open finding. See \[the findings report](findings.md) for the recommended action.



\## Skills demonstrated



\*\*Identity and access management:\*\* comparing granted access with approved permissions and applying least privilege.



\*\*Technical AI governance:\*\* translating ownership and approval requirements into executable checks.



\*\*Governance, risk and compliance:\*\* recording evidence and assigning remediation actions to an accountable team.



The project supports AI security by identifying excessive access and missing oversight controls. It does not evaluate model behaviour or establish overall AI safety.



\## Limitations



This is a configuration-review prototype using fictional data. It does not connect to live systems, remove permissions or verify that human approval is enforced.



Input validation covers selected cases. It is not a complete schema validator, and malformed files or unexpected record structures may cause errors.



Passing checks do not certify compliance or prove that an agent is secure.

