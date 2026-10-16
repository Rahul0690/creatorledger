# CreatorLedger 🇮🇳
**Freelancer invoicing and payment tracking for Indian creators.**

**Created by:** Rahul Singh  
**Project type:** College project / local web application prototype

CreatorLedger is a beginner-friendly Flask + SQLite web app demo. It combines client records, GST-ready invoices, TDS tracking, payment status, a UPI intent link, reminder preparation, and a simple finance report in one responsive interface.

## Project author
This project was created by **Rahul Singh** as a Python Flask web application project.

## Features
- Responsive, animated marketing landing page and app dashboard
- Client directory with contact, address, and GSTIN fields
- Create invoices with subtotal, GST, TDS, net receivable and due date
- Paid / pending / overdue invoice filters
- Invoice detail page with print-to-PDF browser support
- Demo UPI intent link and payment history
- Payment reminder demo flow
- Monthly totals for subtotal, GST, TDS and net receivable
- SQLite database is created automatically; demo data is seeded on first run

## Requirements
- Python 3.10 or newer
- Internet is not required after Python and Flask are installed
- Windows, macOS, or Linux

## Run on Windows (PowerShell)
1. Extract the ZIP.
2. Open the extracted `creatorledger` folder.
3. In File Explorer, click the address bar, type `powershell`, and press Enter.
4. Run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

5. Open **http://127.0.0.1:5000** in Chrome.
6. Use the seeded sample records to demo the app. Create a new client or invoice to show database persistence.

**Shortcut:** double-click `start_windows.bat` to create the virtual environment, install Flask, and start the app. Keep the terminal window open while using the website.

If you prefer not to activate the virtual environment, run the app directly with `\.venv\Scripts\python.exe app.py`. If PowerShell blocks activation, run this once in that terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run on macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000.

## Demo flow for class
1. Open the landing page and click **Open dashboard**.
2. Review billed, received, outstanding and TDS summary cards.
3. Open **Clients** and add a client.
4. Open **Invoices → New invoice** and create an invoice with GST and TDS.
5. Open the invoice detail page to explain subtotal, GST, total, TDS and net receivable.
6. Click **Prepare reminder** to show the demo reminder workflow.
7. Click **Mark as paid** to create a payment history entry.
8. Open **Reports** to show monthly totals.
9. Refresh the page to demonstrate SQLite persistence.

## VS Code Live Server note
CreatorLedger is a Flask application, not a static HTML-only site. VS Code Live Server (commonly port 5500) will show a folder listing or fail to run Flask routes. Start the Python app using the commands above and open `http://127.0.0.1:5000`.

## Push to GitHub
Create an empty repository on GitHub (do not add a README if you already have this README), then run in the project folder:

```powershell
git init
git add .
git commit -m "Build CreatorLedger invoicing app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your repository's real URL. Never commit passwords, API keys, or production secrets. A `.gitignore` is included.

## Important demo / production notes
This is a working **local demo**, not a production accounting or payment service.
- The UPI URI uses a placeholder payee `your-upi-id@bank`. Replace it with your own valid UPI ID before testing with a payment app. No payment is collected or verified by this app.
- Payment reminders are prepared as a demo confirmation; no email/SMS is sent until an email/SMS provider is configured.
- GST/TDS percentages are editable assumptions for demonstration, not tax advice. Ask a qualified accountant about the applicable GST rate, place-of-supply rules, reverse charge, TDS section/rate, thresholds and compliance.
- Before public deployment: configure a strong `FLASK_SECRET_KEY` environment variable, add authentication/authorization, CSRF protection, stronger validation, backups, HTTPS, secure configuration and a proper payment/email integration. Debug mode is off by default; set `FLASK_DEBUG=1` only for local development.
- The local SQLite file `creatorledger.db` is generated at first run and should not be committed if it contains real client information.

## Project structure
```text
creatorledger/
├── app.py
├── requirements.txt
├── README.md
├── DOCUMENTATION.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── clients.html
│   ├── client_form.html
│   ├── invoices.html
│   ├── invoice_form.html
│   ├── invoice_detail.html
│   ├── payments.html
│   ├── reports.html
│   ├── settings.html
│   └── 404.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Automated smoke tests
The repository includes a small `unittest` suite for page rendering, invoice calculations, invalid date rejection, and recording a demo payment. From the project folder, after installing requirements, run:

```powershell
python -m unittest discover -s tests -v
```

The tests use a temporary SQLite database so they do not need to alter your real demo database. They still require Flask to be installed in the active Python environment.

## Author credit
**Created by Rahul Singh** · CreatorLedger educational project.
