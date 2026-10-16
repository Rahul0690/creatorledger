"""Smoke tests for CreatorLedger's core local-demo workflows."""
import os
import tempfile
import unittest
from pathlib import Path

# Set the database path before importing the application so tests never touch local user data.
_TEST_DB_DIR = tempfile.TemporaryDirectory(prefix="creatorledger-tests-")
os.environ["CREATORLEDGER_DB_PATH"] = str(Path(_TEST_DB_DIR.name) / "test_creatorledger.db")
import app as creator_app


class CreatorLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        creator_app.app.config.update(TESTING=True)
        creator_app.init_db()
        cls.client = creator_app.app.test_client()

    @classmethod
    def tearDownClass(cls):
        _TEST_DB_DIR.cleanup()

    def test_main_pages_render(self):
        for path in ("/", "/dashboard", "/clients", "/invoices", "/payments", "/reports", "/settings"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_invoice_creation_and_demo_payment(self):
        with creator_app.db() as conn:
            client_id = conn.execute("SELECT id FROM clients ORDER BY id LIMIT 1").fetchone()[0]
        response = self.client.post("/invoices/new", data={
            "client_id": str(client_id),
            "title": "Automated test service",
            "issue_date": "2026-10-17",
            "due_date": "2026-10-24",
            "subtotal": "10000",
            "gst_rate": "18",
            "tds_rate": "10",
            "notes": "Test only",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"INV-", response.data)
        with creator_app.db() as conn:
            invoice = conn.execute("SELECT * FROM invoices WHERE title=?", ("Automated test service",)).fetchone()
        self.assertIsNotNone(invoice)
        self.assertAlmostEqual(invoice["gst_amount"], 1800.0)
        self.assertAlmostEqual(invoice["total"], 11800.0)
        self.assertAlmostEqual(invoice["tds_amount"], 1000.0)
        self.assertAlmostEqual(invoice["net_receivable"], 10800.0)
        paid_response = self.client.post(f"/invoices/{invoice['id']}/mark-paid", data={
            "method": "UPI", "reference": "UNIT-TEST-001"
        }, follow_redirects=True)
        self.assertEqual(paid_response.status_code, 200)
        with creator_app.db() as conn:
            updated = conn.execute("SELECT status FROM invoices WHERE id=?", (invoice["id"],)).fetchone()
            payments = conn.execute("SELECT COUNT(*) FROM payments WHERE invoice_id=?", (invoice["id"],)).fetchone()[0]
        self.assertEqual(updated["status"], "Paid")
        self.assertEqual(payments, 1)

    def test_invoice_rejects_due_date_before_issue_date(self):
        with creator_app.db() as conn:
            client_id = conn.execute("SELECT id FROM clients ORDER BY id LIMIT 1").fetchone()[0]
        response = self.client.post("/invoices/new", data={
            "client_id": str(client_id), "title": "Invalid dates",
            "issue_date": "2026-10-20", "due_date": "2026-10-19",
            "subtotal": "1000", "gst_rate": "18", "tds_rate": "10",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Due date must be on or after issue date", response.data)
        with creator_app.db() as conn:
            count = conn.execute("SELECT COUNT(*) FROM invoices WHERE title='Invalid dates'").fetchone()[0]
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
