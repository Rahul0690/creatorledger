# CreatorLedger 🇮🇳

**Freelancer invoicing and payment tracking for Indian creators.**

🌐 **[Open Live Website](https://creatorledger-0t89.onrender.com)** · 💻 **[View GitHub Repository](https://github.com/Rahul0690/creatorledger)**

## Overview

CreatorLedger is a Python Flask and SQLite web application prototype that brings client records, invoices, payment tracking, and financial summaries into one responsive interface.

## Features

- Responsive landing page and dashboard
- Client directory with contact and GSTIN details
- Invoice creation with subtotal, GST, TDS, net receivable, and due dates
- Invoice status views and filters
- Invoice detail page with browser print-to-PDF support
- Demo UPI intent link and payment history
- Demo payment-reminder preparation
- Monthly financial reports
- SQLite database and sample-data setup

## Technology Stack

- Python
- Flask
- SQLite
- HTML, CSS and JavaScript
- Git and GitHub
- Gunicorn
- Render

## Installation and Setup

### Windows

**1.** Open the project folder in VS Code and open its terminal.

**2.** Create a virtual environment:

```powershell
py -m venv .venv
```

**3.** Install the dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**4.** Start the application:

```powershell
.\.venv\Scripts\python.exe app.py
```

**5.** Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser if that address is shown in the terminal.

Keep the terminal open while using the application. Press `Ctrl+C` to stop the local server.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Application Modules

| Module | Purpose |
|---|---|
| Dashboard | Summary figures and recent invoice activity |
| Clients | Client directory and contact details |
| Invoices | Invoice records, amounts, due dates and statuses |
| Payments | Recorded payment history |
| Reports | Financial summaries and monthly breakdown |
| Print Preview | Print or save a report using the browser |

## Screenshots

The project documentation covers these seven interface views:

1. Landing page
2. Dashboard
3. Client directory
4. Invoice list
5. Payment history
6. Financial reports
7. Browser print preview

See [`docs/SCREENSHOTS.md`](docs/SCREENSHOTS.md) for screenshot descriptions and suggested filenames.

To display images directly in GitHub, upload them to `docs/screenshots/` and reference them using relative Markdown links.

## Deployment

CreatorLedger is deployed on Render.

- **Live website:** [creatorledger-0t89.onrender.com](https://creatorledger-0t89.onrender.com)
- **Source code:** [github.com/Rahul0690/creatorledger](https://github.com/Rahul0690/creatorledger)
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`

Make sure `requirements.txt` includes both Flask and Gunicorn. After pushing changes to GitHub, check the latest deployment logs on Render.

The free hosting service may take longer to respond after inactivity.

For more details, see [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Testing

The repository describes a `unittest` suite for page rendering, invoice calculations, invalid-date handling, and demo-payment recording.

Run the tests from the project folder:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Only report tests as passing after running the command and checking the output.

## Important Limitations

- This is an educational/demo prototype, not a production accounting or payment service.
- Sample records and amounts should not be treated as real financial data.
- The demo UPI link does not verify or collect payments.
- Reminder preparation does not send email or SMS unless a provider is configured.
- GST and TDS values are demonstration estimates, not tax advice.
- Authentication, security, backups, and other production requirements must be verified before public real-world use.

## Future Improvements

- Expand automated testing and validation.
- Improve data backup and monitoring.
- Add invoice and report export options.
- Add verified email reminders.
- Review authentication and security before production use.

## Useful Links

- [Live Demo](https://creatorledger-0t89.onrender.com)
- [GitHub Repository](https://github.com/Rahul0690/creatorledger)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/3/)
- [Render Documentation](https://render.com/docs)
- [GitHub Documentation](https://docs.github.com/)

---

**Created by Rahul Singh** · CreatorLedger educational project.
