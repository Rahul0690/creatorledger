# CreatorLedger — Project Process Documentation

**Project type:** Full-stack web application prototype  
**Domain:** Freelancer invoicing and payment tracking for Indian creators  
**Technology:** Python, Flask, SQLite, HTML, CSS, JavaScript  
**Created by:** Rahul Singh  
**Prepared for:** College project demonstration

**Project status:** Local prototype / educational demonstration

## Project author
CreatorLedger was created by **Rahul Singh**. The application is an educational prototype intended to demonstrate Python Flask web development, SQLite persistence, invoice calculations and payment-status tracking.

## 1. Abstract
Independent creators and freelancers need a simple way to manage client details, issue invoices, track payment status, and estimate GST and TDS effects. Many generic invoicing tools focus on other markets or separate these tasks across different products. CreatorLedger is a lightweight web prototype that brings these tasks into one interface.

## 2. Problem statement
Freelancers may track client details in one place, create invoices in another, and chase pending payments manually. This can make it difficult to see how much has been billed, received, or remains outstanding. GST and TDS details also need to be visible when estimating the amount due.

## 3. Objectives
- Build a modern, animated and responsive website.
- Store client, invoice and payment data in a database.
- Calculate invoice subtotal, GST, TDS, total and net receivable.
- Show paid, pending and overdue invoice states.
- Provide a demo UPI payment intent link.
- Provide a reminder workflow and monthly report.
- Keep the project easy to run locally and push to GitHub.

## 4. Scope
### Included
Client management; invoice creation; GST/TDS calculations; invoice filtering; payment tracking; dashboard totals; UPI intent link; reminder demo flow; monthly summary; browser print support.

### Not included in this prototype
Real payment settlement/verification, automatic email/SMS delivery, user accounts, multi-business tenancy, e-invoice/IRN generation, GST portal integration, bank reconciliation, production hosting and legally validated tax logic.

## 5. Tools and technologies
- **Python:** application logic and calculations.
- **Flask:** routes, request handling and HTML rendering.
- **SQLite:** local relational database.
- **HTML/Jinja:** reusable templates and dynamic pages.
- **CSS:** responsive layout, gradients, hover effects and entrance animations.
- **JavaScript:** mobile navigation, UI helpers and invoice calculation preview.
- **Git/GitHub:** source control and project submission.

## 6. System architecture
The browser requests a page from the Flask application. Flask validates form values, reads/writes records using SQLite, calculates totals, and renders a Jinja template. The browser then displays the responsive UI.

```text
User / Browser
      |
      v
HTML + CSS + JavaScript
      |
      v
Flask routes and validation
      |
      v
SQLite database
  | clients
  | invoices
  | payments
```

## 7. Database design
### clients
| Field | Purpose |
|---|---|
| id | Primary key |
| name | Client or business name |
| email, phone | Contact information |
| business | Business name |
| gstin | Optional GST identification number |
| address | Billing address |
| created_at | Creation date |

### invoices
| Field | Purpose |
|---|---|
| id | Primary key |
| invoice_no | Unique invoice identifier |
| client_id | Foreign key to clients |
| title | Work/service description |
| issue_date, due_date | Invoice dates |
| subtotal | Service amount before GST |
| gst_rate, gst_amount | GST assumption and calculated amount |
| tds_rate, tds_amount | TDS assumption and calculated deduction |
| total | Subtotal + GST |
| net_receivable | Total − TDS |
| notes | Additional invoice notes |
| status | Paid or Pending |

### payments
| Field | Purpose |
|---|---|
| id | Primary key |
| invoice_id | Related invoice |
| amount | Payment amount |
| method | Payment method label |
| paid_on | Recorded payment date |
| reference | Demo transaction reference |

## 8. Calculation logic
For the simple demo case:
- `GST amount = subtotal × GST rate ÷ 100`
- `Invoice total = subtotal + GST amount`
- `TDS amount = subtotal × TDS rate ÷ 100`
- `Net receivable = invoice total − TDS amount`

**Example:** For a service subtotal of ₹10,000, GST at 18% and TDS at 10%:
- GST = ₹1,800
- Invoice total = ₹11,800
- TDS estimate = ₹1,000
- Net receivable estimate = ₹10,800

These are illustrative calculations only. Actual tax treatment depends on the transaction, service, jurisdiction, applicable law and the client's circumstances.

## 9. Main user workflow
1. Open the landing page.
2. Open the dashboard and review the summary.
3. Add a client with contact and optional GSTIN information.
4. Create an invoice with issue/due dates and tax-rate assumptions.
5. Review the invoice detail and print it from the browser if required.
6. Prepare a payment reminder (demo only).
7. Record a payment by marking the invoice as paid.
8. View payment history and monthly reports.

## 10. Interface and design
The interface uses a clean SaaS visual language: dark ink typography, violet accent gradients, soft surfaces, rounded cards, subtle motion and a responsive navigation system. Animation is designed to support hierarchy rather than interfere with reading. The layout adapts to desktop and mobile screens. The invoice form defaults the due date to 14 days after the current date. The Flask debug server is disabled by default; `FLASK_DEBUG=1` can be used for local debugging only.

The visual direction is inspired by contemporary SaaS landing-page patterns; no specific Framer template assets are included.

## 11. Testing checklist
Run these checks on the target laptop after setup. These are a manual verification checklist; do not mark a check as passed until you have performed it:
- [ ] Install dependencies with `python -m pip install -r requirements.txt`.
- [ ] Start with `python app.py`; terminal should show the local address.
- [ ] Open the homepage and dashboard.
- [ ] Add a client; verify it appears in Clients.
- [ ] Create an invoice with subtotal ₹10,000, GST 18%, TDS 10%; expect GST ₹1,800, total ₹11,800, TDS ₹1,000 and net ₹10,800.
- [ ] Verify the invoice is listed as Pending.
- [ ] Use Prepare reminder and confirm the demo message appears.
- [ ] Mark the invoice as Paid and verify a payment entry appears.
- [ ] Open Reports and confirm the invoice is included.
- [ ] Restart the app and verify records persist in SQLite.

## 12. Running the application correctly
CreatorLedger must be started with Python/Flask. VS Code Live Server is intended for static HTML pages and does not run Flask routes or SQLite logic. On Windows, run `start_windows.bat` or execute `python app.py` from the activated virtual environment, then open `http://127.0.0.1:5000`. Keep the terminal open while the application is in use.

## 13. GitHub submission process
1. Create a repository on GitHub.
2. Open PowerShell inside the extracted project folder.
3. Run:
   ```powershell
   git init
   git add .
   git commit -m "Build CreatorLedger invoicing app"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   git push -u origin main
   ```
4. Replace the example remote with the URL shown by GitHub.
5. Verify the files are visible in the repository.
6. Include the README and this document in the submission.

## 14. Limitations and future scope
- Authentication and separate creator/client roles.
- Real payment gateway and verified webhooks.
- Email/SMS reminders with consent and delivery logs.
- Export to PDF/CSV and accounting software integration.
- Configurable invoice branding and business profile.
- Tax rules validated by a qualified professional.
- Production database, automated backups, audit logs, security hardening and deployment.

## 15. Conclusion
CreatorLedger demonstrates the core workflow of a freelancer invoicing and payment tracking system with a modern interface and persistent relational storage. It provides a foundation for further development while keeping external payment and messaging services clearly marked as integrations to add later.

## 16. Automated smoke tests
The project includes a `unittest` smoke-test suite under `tests/test_app.py`. It checks that primary pages render, verifies the example GST/TDS arithmetic, tests that an invalid due date is rejected, and checks that the demo payment workflow updates an invoice and creates a payment record. Run it after installing `requirements.txt`:

```powershell
python -m unittest discover -s tests -v
```

The test suite redirects database access to a temporary database. It is a useful regression check, not a replacement for manual browser testing on Windows and mobile screen sizes.

## 17. Author credit
**Created by Rahul Singh.** CreatorLedger is an educational portfolio/college project. Any future submission should follow the institution's own formatting rules and include actual screenshots from the final local run if required.
