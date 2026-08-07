"""create mock data

Revision ID: de88c2999a75
Revises: 334757f7b99a
Create Date: 2026-08-07 11:50:35.353460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de88c2999a75'
down_revision: Union[str, Sequence[str], None] = '334757f7b99a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Insert External Law Firms
    op.execute("""
            INSERT INTO firm (name, contact_email, status) VALUES 
            ('LexCorp Legal Partners', 'billing@lexcorplegal.com', 'active'),
            ('Apex Litigation Group', 'invoices@apexlitigation.com', 'active'),
            ('Vanguard Counsel LLP', 'accounts@vanguardcounsel.com', 'active');
        """)

    # 2. Insert Users (Internal and Firm-scoped)
    op.execute("""
            INSERT INTO "user" (name, email, password_hash, role, firm_id) VALUES 
            ('Rajat Bombale', 'rajat.bombale@company.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin', NULL),
            ('Trinkesh Ops', 'trinkesh@company.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'editor', NULL),
            ('Bhushan Auditor', 'bhushan@company.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'viewer', NULL),
            ('Firm Admin LexCorp', 'admin@lexcorplegal.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'editor', 1);
        """)

    # 3. Insert Matters
    op.execute("""
            INSERT INTO matter (firm_id, name, owner, status) VALUES 
            (1, 'Project Titan IP Defense', 'Rajat Bombale', 'open'),
            (2, 'Global Compliance Restructuring', 'Trinkesh Ops', 'open'),
            (3, 'Supply Chain Antitrust Review', 'Rajat Bombale', 'open');
        """)

    # 4. Insert Budgets (1:1 with Matters)
    op.execute("""
            INSERT INTO budget (matter_id, allocated_amt, threshold_pct) VALUES 
            (1, 50000.00, 80.0),
            (2, 35000.00, 75.0),
            (3, 20000.00, 80.0);
        """)

    # 5. Insert Invoices
    op.execute("""
            INSERT INTO invoice (matter_id, firm_id, invoice_no, invoice_date, total_amount, status, confidence_score) VALUES 
            (1, 1, 'INV-2026-001', '2026-06-15', 12500.00, 'approved', 0.98),
            (1, 1, 'INV-2026-002', '2026-07-10', 15000.00, 'approved', 0.95),
            (2, 2, 'APEX-9921', '2026-07-01', 28000.00, 'pending_review', 0.89);
        """)

    # 6. Insert Line Items
    op.execute("""
            INSERT INTO line_item (invoice_id, timekeeper, hours, rate, amount) VALUES 
            (1, 'Sarah Jenkins (Partner)', 10.0, 750.00, 7500.00),
            (1, 'Mark Vance (Associate)', 20.0, 250.00, 5000.00),
            (2, 'Sarah Jenkins (Partner)', 15.0, 750.00, 11250.00),
            (2, 'Elena Rostova (Paralegal)', 25.0, 150.00, 3750.00),
            (3, 'David Thorne (Senior Partner)', 35.0, 800.00, 28000.00);
        """)

    # 7. Insert Budget Ledgers
    op.execute("""
            INSERT INTO budget_ledger (budget_id, invoice_id, amount, entry_type, created_at) VALUES 
            (1, 1, 12500.00, 'invoice_approved', '2026-06-18T10:30:00Z'),
            (1, 2, 15000.00, 'invoice_approved', '2026-07-12T14:15:00Z');
        """)

    # 8. Insert Threshold Alerts
    op.execute("""
            INSERT INTO alert (budget_id, type, message, created_at) VALUES 
            (1, 'threshold_warning', 'Matter #1 has crossed 50% utilization ($27,500 / $50,000).', '2026-07-12T14:15:05Z');
        """)

    # 9. Insert Audit Logs
    op.execute("""
            INSERT INTO audit_log (invoice_id, user_id, action, notes, timestamp) VALUES 
            (1, 3, 'extracted', 'Automated OCR extraction successful with 0.98 confidence.', '2026-06-15T09:00:00Z'),
            (1, 1, 'approved', 'Verified line items against rate card. Approved for ledger posting.', '2026-06-18T10:30:00Z'),
            (3, -1, 'extracted', 'Automated extraction completed.', '2026-07-01T11:20:00Z');
        """)


def downgrade() -> None:
  # Clean up mock data in reverse dependency sequence one statement at a time
  op.execute("DELETE FROM audit_log;")
  op.execute("DELETE FROM alert;")
  op.execute("DELETE FROM budget_ledger;")
  op.execute("DELETE FROM line_item;")
  op.execute("DELETE FROM invoice;")
  op.execute("DELETE FROM budget;")
  op.execute("DELETE FROM matter;")
  op.execute('DELETE FROM "user";')
  op.execute("DELETE FROM firm;")