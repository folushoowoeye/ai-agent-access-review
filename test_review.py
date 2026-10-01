import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).resolve().with_name("review.py")


class AccessReviewTests(unittest.TestCase):
    def setUp(self):
        self.agent = {
            "agent_id": "test-agent",
            "owner": "Test Team",
            "permissions": ["tickets:read"],
            "human_approval_enabled_for": []
        }
        self.policy = {
            "approved_permissions": ["tickets:read"],
            "approval_expires": "2099-12-31",
            "human_approval_required_for": []
        }

    def run_review(self):
        with tempfile.TemporaryDirectory() as folder:
            test_folder = Path(folder)

            (test_folder / "agents.json").write_text(
                json.dumps([self.agent]), encoding="utf-8"
            )
            (test_folder / "policy.json").write_text(
                json.dumps({"test-agent": self.policy}),
                encoding="utf-8"
            )

            result = subprocess.run(
                [sys.executable, str(CHECKER)],
                cwd=test_folder,
                capture_output=True,
                text=True
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_approved_permissions_pass(self):
        output = self.run_review()
        self.assertIn(
            "PASS: No permissions exceed approved access.", output
        )
        self.assertNotIn("FINDING:", output)
        self.assertNotIn("NEEDS REVIEW:", output)

    def test_excessive_permission_is_flagged(self):
        self.agent["permissions"].append("tickets:delete")
        output = self.run_review()
        self.assertIn(
            "Remove or seek approval for: tickets:delete", output
        )
        self.assertNotIn(
            "PASS: No permissions exceed approved access.", output
        )

    def test_blank_owner_is_flagged(self):
        self.agent["owner"] = " "
        output = self.run_review()
        self.assertIn("FINDING: No accountable owner recorded.", output)

    def test_expired_approval_is_flagged(self):
        self.policy["approval_expires"] = "2000-01-01"
        output = self.run_review()
        self.assertIn(
            "FINDING: Access approval expired on 2000-01-01.", output
        )

    def test_missing_human_approval_is_flagged(self):
        self.agent["permissions"] = ["payments:execute"]
        self.policy["approved_permissions"] = ["payments:execute"]
        self.policy["human_approval_required_for"] = ["payments:execute"]
        output = self.run_review()
        self.assertIn(
            "FINDING: Human approval missing for: payments:execute",
            output
        )
        self.assertNotIn(
            "PASS: No required human approval controls are missing.",
            output
        )

    def test_unknown_approval_requirements_need_review(self):
        self.policy["human_approval_required_for"] = None
        output = self.run_review()
        self.assertIn("NEEDS REVIEW: Human approval records", output)
        self.assertNotIn(
            "PASS: No required human approval controls are missing.",
            output
        )

    def test_unknown_permissions_need_review(self):
        self.agent["permissions"] = None
        output = self.run_review()
        self.assertIn("NEEDS REVIEW: Permissions must be lists", output)
        self.assertIn("SKIPPED: Human approval check", output)
        self.assertNotIn(
            "PASS: No permissions exceed approved access.", output
        )

    def test_invalid_expiry_date_needs_review(self):
        self.policy["approval_expires"] = "not-a-date"
        output = self.run_review()
        self.assertIn(
            "NEEDS REVIEW: Approval expiry date is invalid.", output
        )


if __name__ == "__main__":
    unittest.main()