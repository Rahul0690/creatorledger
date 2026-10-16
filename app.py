from flask import Flask, render_template, request, redirect, url_for, flash, abort
import sqlite3
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
import os

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("CREATORLEDGER_DB_PATH", BASE_DIR / "creatorledger.db")).expanduser().resolve()
app = Flask(__name__)
# Local-demo fallback only. Set FLASK_SECRET_KEY to a long random value before deployment.
# A configured secret is recommended. A random local fallback avoids shipping a fixed secret.
# Set FLASK_SECRET_KEY to a stable random value if you need sessions to survive restarts.
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            business TEXT DEFAULT '',
            gstin TEXT DEFAULT '',
            address TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT NOT NULL UNIQUE,
            client_id INTEGER NOT NULL REFERENCES clients(id),
            title TEXT NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            subtotal REAL NOT NULL DEFAULT 0,
            gst_rate REAL NOT NULL DEFAULT 0,
            gst_amount REAL NOT NULL DEFAULT 0,
            tds_rate REAL NOT NULL DEFAULT 0,
            tds_amount REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL DEFAULT 0,
            net_receivable REAL NOT NULL DEFAULT 0,
            notes TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER NOT NULL REFERENCES invoices(id),
            amount REAL NOT NULL,
            method TEXT NOT NULL DEFAULT 'UPI',
            paid_on TEXT NOT NULL,
            reference TEXT DEFAULT ''
        );
        """)
        count = conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
        if count == 0:
            today = date.today()
            c1 = conn.execute("""INSERT INTO clients(name,email,phone,business,gstin,address,created_at)
                VALUES(?,?,?,?,?,?,?)""",
                ("Aarav Mehta", "aarav@example.com", "+91 98765 43210", "Mehta Media", "27ABCDE1234F1Z5", "Pune, Maharashtra", today.isoformat())).lastrowid
            c2 = conn.execute("""INSERT INTO clients(name,email,phone,business,gstin,address,created_at)
                VALUES(?,?,?,?,?,?,?)""",
                ("Studio North", "accounts@studionorth.example", "+91 91234 56780", "Studio North", "", "Mumbai, Maharashtra", today.isoformat())).lastrowid
            invs = [
                ("INV-2026-001", c1, "Brand identity design", (today-timedelta(days=20)).isoformat(), (today-timedelta(days=6)).isoformat(), 25000, 18, 10, "Logo, brand kit and social templates", "Paid"),
                ("INV-2026-002", c2, "Website UI design", (today-timedelta(days=4)).isoformat(), (today+timedelta(days=10)).isoformat(), 42000, 18, 10, "Landing page and responsive dashboard", "Pending"),
                ("INV-2026-003", c1, "Social media creatives", today.isoformat(), (today+timedelta(days=14)).isoformat(), 12000, 18, 0, "Monthly creative pack", "Pending"),
            ]
            for no, cid, title, issue, due, subtotal, gst, tds, notes, status in invs:
                gst_amount = round(subtotal*gst/100, 2)
                tds_amount = round(subtotal*tds/100, 2)
                total = round(subtotal+gst_amount, 2)
                net = round(total-tds_amount, 2)
                cur = conn.execute("""INSERT INTO invoices(invoice_no,client_id,title,issue_date,due_date,subtotal,gst_rate,gst_amount,tds_rate,tds_amount,total,net_receivable,notes,status,created_at)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (no,cid,title,issue,due,subtotal,gst,gst_amount,tds,tds_amount,total,net,notes,status,today.isoformat()))
                if status == "Paid":
                    conn.execute("INSERT INTO payments(invoice_id,amount,method,paid_on,reference) VALUES(?,?,?,?,?)",
                                 (cur.lastrowid, net, "UPI", today.isoformat(), "DEMO-UPI-001"))

def money(value):
    return f"₹{float(value or 0):,.2f}"

app.jinja_env.filters["money"] = money

@app.context_processor
def inject_globals():
    return {"today": date.today().isoformat(), "default_due_date": (date.today() + timedelta(days=14)).isoformat()}

@app.route("/")
def home():
    with db() as conn:
        stats = conn.execute("""SELECT COUNT(*) AS count, COALESCE(SUM(total),0) AS billed,
            COALESCE(SUM(CASE WHEN status='Paid' THEN net_receivable ELSE 0 END),0) AS received,
            COALESCE(SUM(CASE WHEN status!='Paid' THEN net_receivable ELSE 0 END),0) AS outstanding
            FROM invoices""").fetchone()
        recent = conn.execute("""SELECT i.*, c.name AS client_name FROM invoices i JOIN clients c ON c.id=i.client_id
            ORDER BY i.id DESC LIMIT 4""").fetchall()
    return render_template("index.html", stats=stats, recent=recent)

@app.route("/dashboard")
def dashboard():
    with db() as conn:
        stats = conn.execute("""SELECT COUNT(*) AS invoice_count,
            COALESCE(SUM(total),0) AS billed,
            COALESCE(SUM(CASE WHEN status='Paid' THEN net_receivable ELSE 0 END),0) AS received,
            COALESCE(SUM(CASE WHEN status!='Paid' THEN net_receivable ELSE 0 END),0) AS outstanding,
            COALESCE(SUM(tds_amount),0) AS tds FROM invoices""").fetchone()
        recent = conn.execute("""SELECT i.*, c.name AS client_name FROM invoices i JOIN clients c ON c.id=i.client_id
            ORDER BY i.id DESC LIMIT 6""").fetchall()
        overdue = conn.execute("""SELECT COUNT(*) FROM invoices WHERE status!='Paid' AND due_date < ?""", (date.today().isoformat(),)).fetchone()[0]
    return render_template("dashboard.html", stats=stats, recent=recent, overdue=overdue)

@app.route("/clients")
def clients():
    with db() as conn:
        rows = conn.execute("""SELECT c.*, COUNT(i.id) AS invoice_count,
            COALESCE(SUM(i.total),0) AS billed FROM clients c LEFT JOIN invoices i ON i.client_id=c.id
            GROUP BY c.id ORDER BY c.id DESC""").fetchall()
    return render_template("clients.html", clients=rows)

@app.route("/clients/new", methods=["GET", "POST"])
def new_client():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        if not name:
            flash("Client name is required.", "error")
            return render_template("client_form.html", client=None)
        with db() as conn:
            conn.execute("""INSERT INTO clients(name,email,phone,business,gstin,address,created_at)
                VALUES(?,?,?,?,?,?,?)""", (name, request.form.get("email","").strip(),
                request.form.get("phone","").strip(), request.form.get("business","").strip(),
                request.form.get("gstin","").strip().upper(), request.form.get("address","").strip(),
                date.today().isoformat()))
        flash("Client saved successfully.", "success")
        return redirect(url_for("clients"))
    return render_template("client_form.html", client=None)

@app.route("/clients/<int:client_id>/edit", methods=["GET", "POST"])
def edit_client(client_id):
    with db() as conn:
        client = conn.execute("SELECT * FROM clients WHERE id=?", (client_id,)).fetchone()
        if not client: abort(404)
        if request.method == "POST":
            name = request.form.get("name","").strip()
            if not name:
                flash("Client name is required.", "error")
                return render_template("client_form.html", client=client)
            conn.execute("""UPDATE clients SET name=?,email=?,phone=?,business=?,gstin=?,address=? WHERE id=?""",
                (name,request.form.get("email","").strip(),request.form.get("phone","").strip(),
                 request.form.get("business","").strip(),request.form.get("gstin","").strip().upper(),
                 request.form.get("address","").strip(),client_id))
        else:
            return render_template("client_form.html", client=client)
    flash("Client updated.", "success")
    return redirect(url_for("clients"))

def next_invoice_number(conn):
    year = date.today().year
    count = conn.execute("SELECT COUNT(*) FROM invoices WHERE invoice_no LIKE ?", (f"INV-{year}-%",)).fetchone()[0] + 1
    return f"INV-{year}-{count:03d}"

@app.route("/invoices")
def invoices():
    status = request.args.get("status","")
    with db() as conn:
        if status in ("Paid","Pending","Overdue"):
            if status == "Overdue":
                rows = conn.execute("""SELECT i.*,c.name client_name FROM invoices i JOIN clients c ON c.id=i.client_id
                    WHERE i.status!='Paid' AND i.due_date < ? ORDER BY i.id DESC""", (date.today().isoformat(),)).fetchall()
            else:
                rows = conn.execute("""SELECT i.*,c.name client_name FROM invoices i JOIN clients c ON c.id=i.client_id
                    WHERE i.status=? ORDER BY i.id DESC""", (status,)).fetchall()
        else:
            rows = conn.execute("""SELECT i.*,c.name client_name FROM invoices i JOIN clients c ON c.id=i.client_id
                ORDER BY i.id DESC""").fetchall()
    return render_template("invoices.html", invoices=rows, active_status=status)

@app.route("/invoices/new", methods=["GET","POST"])
def new_invoice():
    with db() as conn:
        client_rows = conn.execute("SELECT * FROM clients ORDER BY name").fetchall()
        if not client_rows:
            flash("Add a client before creating an invoice.", "error")
            return redirect(url_for("new_client"))
        if request.method == "POST":
            try:
                client_id = int(request.form.get("client_id", "0"))
                subtotal_decimal = Decimal(request.form.get("subtotal", "0").strip())
                gst_decimal = Decimal(request.form.get("gst_rate", "0").strip())
                tds_decimal = Decimal(request.form.get("tds_rate", "0").strip())
                if not all(value.is_finite() for value in (subtotal_decimal, gst_decimal, tds_decimal)):
                    raise ValueError
                if subtotal_decimal <= 0 or subtotal_decimal > Decimal("100000000"):
                    raise ValueError
                if not (0 <= gst_decimal <= 100) or not (0 <= tds_decimal <= 100):
                    raise ValueError
                issue_date = date.fromisoformat(request.form.get("issue_date") or date.today().isoformat())
                due_date = date.fromisoformat(request.form.get("due_date") or (date.today() + timedelta(days=14)).isoformat())
                if due_date < issue_date:
                    raise ValueError
                title = request.form.get("title", "").strip()
                if not title or len(title) > 180:
                    raise ValueError
                client = conn.execute("SELECT id FROM clients WHERE id=?", (client_id,)).fetchone()
                if not client:
                    raise ValueError
                subtotal = float(subtotal_decimal)
                gst_rate = float(gst_decimal)
                tds_rate = float(tds_decimal)
            except (ValueError, InvalidOperation):
                flash("Check the client, service name, dates and amount. Due date must be on or after issue date; rates must be between 0 and 100.", "error")
                return render_template("invoice_form.html", clients=client_rows, invoice=None)
            gst_amount = round(subtotal*gst_rate/100,2)
            tds_amount = round(subtotal*tds_rate/100,2)
            total = round(subtotal+gst_amount,2)
            net = round(total-tds_amount,2)
            invoice_no = next_invoice_number(conn)
            conn.execute("""INSERT INTO invoices(invoice_no,client_id,title,issue_date,due_date,subtotal,gst_rate,gst_amount,tds_rate,tds_amount,total,net_receivable,notes,status,created_at)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,'Pending',?)""",
                (invoice_no,client_id,title,issue_date.isoformat(),due_date.isoformat(),
                 subtotal,gst_rate,gst_amount,tds_rate,tds_amount,total,net,request.form.get("notes","").strip()[:2000],date.today().isoformat()))
        else:
            return render_template("invoice_form.html", clients=client_rows, invoice=None)
    flash(f"Invoice {invoice_no} created.", "success")
    return redirect(url_for("invoice_detail", invoice_id=conn.execute("SELECT id FROM invoices WHERE invoice_no=?", (invoice_no,)).fetchone()[0]))

@app.route("/invoices/<int:invoice_id>")
def invoice_detail(invoice_id):
    with db() as conn:
        invoice = conn.execute("""SELECT i.*,c.name client_name,c.email client_email,c.phone client_phone,
            c.business client_business,c.gstin client_gstin,c.address client_address
            FROM invoices i JOIN clients c ON c.id=i.client_id WHERE i.id=?""", (invoice_id,)).fetchone()
        if not invoice: abort(404)
        payments = conn.execute("SELECT * FROM payments WHERE invoice_id=? ORDER BY id DESC", (invoice_id,)).fetchall()
    upi = f"upi://pay?pa=your-upi-id@bank&pn=CreatorLedger&am={invoice['net_receivable']:.2f}&cu=INR&tn={invoice['invoice_no']}"
    return render_template("invoice_detail.html", invoice=invoice, payments=payments, upi_link=upi)

@app.route("/invoices/<int:invoice_id>/mark-paid", methods=["POST"])
def mark_paid(invoice_id):
    with db() as conn:
        inv = conn.execute("SELECT * FROM invoices WHERE id=?", (invoice_id,)).fetchone()
        if not inv: abort(404)
        if inv["status"] != "Paid":
            allowed_methods = {"UPI", "Bank transfer", "Cash", "Other"}
            method = request.form.get("method", "UPI")
            if method not in allowed_methods:
                flash("Choose a valid payment method.", "error")
                return redirect(url_for("invoice_detail", invoice_id=invoice_id))
            reference = request.form.get("reference", "").strip()[:120] or "DEMO-PAYMENT"
            conn.execute("UPDATE invoices SET status='Paid' WHERE id=?", (invoice_id,))
            conn.execute("INSERT INTO payments(invoice_id,amount,method,paid_on,reference) VALUES(?,?,?,?,?)",
                (invoice_id,inv["net_receivable"],method,date.today().isoformat(),reference))
    flash("Invoice marked as paid in demo mode.", "success")
    return redirect(url_for("invoice_detail", invoice_id=invoice_id))

@app.route("/invoices/<int:invoice_id>/reminder", methods=["POST"])
def reminder(invoice_id):
    with db() as conn:
        inv = conn.execute("""SELECT i.*,c.email FROM invoices i JOIN clients c ON c.id=i.client_id WHERE i.id=?""", (invoice_id,)).fetchone()
        if not inv: abort(404)
    # Demo-only: prepares reminder text; no email is sent without an email provider.
    flash(f"Demo reminder prepared for {inv['email'] or 'client'} — connect an email provider to send it.", "success")
    return redirect(url_for("invoice_detail", invoice_id=invoice_id))

@app.route("/payments")
def payments():
    with db() as conn:
        rows = conn.execute("""SELECT p.*,i.invoice_no,i.title,c.name client_name FROM payments p
            JOIN invoices i ON i.id=p.invoice_id JOIN clients c ON c.id=i.client_id ORDER BY p.id DESC""").fetchall()
        total = conn.execute("SELECT COALESCE(SUM(amount),0) FROM payments").fetchone()[0]
    return render_template("payments.html", payments=rows, total=total)

@app.route("/reports")
def reports():
    with db() as conn:
        rows = conn.execute("""SELECT strftime('%Y-%m', issue_date) month, COUNT(*) count,
            COALESCE(SUM(subtotal),0) subtotal,COALESCE(SUM(gst_amount),0) gst,
            COALESCE(SUM(tds_amount),0) tds,COALESCE(SUM(net_receivable),0) net
            FROM invoices GROUP BY month ORDER BY month DESC""").fetchall()
        totals = conn.execute("""SELECT COALESCE(SUM(subtotal),0) subtotal, COALESCE(SUM(gst_amount),0) gst,
            COALESCE(SUM(tds_amount),0) tds, COALESCE(SUM(net_receivable),0) net FROM invoices""").fetchone()
    return render_template("reports.html", rows=rows, totals=totals)

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

init_db()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
