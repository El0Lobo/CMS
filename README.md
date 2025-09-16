# Bar OS Starter — Full Template Pass (Windows + psycopg + CMS)

This starter adds **templates & placeholder pages for every module** so you
can immediately see the shape of the app and grow each part.

## Highlights
- CMS Login (`/accounts/login/`) + **Dashboard** (`/dashboard/`)
- **Left-hand CMS nav** with sections for: Pages, Blog, Events, Shifts, Door,
  POS, Merch, Inventory, Accounting, Social, Automation (Home Assistant), Maps, Settings
- **Public**: Home (`/`), Theme demo (`/theme-demo/`), Events list (`/events/`) and detail (`/events/sample-event/`)
- psycopg (v3) included; Postgres ready (via Docker) or use SQLite locally

## Run (PowerShell)
```powershell
.\scripts\dev_windows.ps1
python manage.py create_dev_admin --username admin --email admin@example.com --password admin123
```

## Switch to Postgres (optional)
```powershell
docker compose up -d db redis
# set in .env:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
.\scripts\dev_windows.ps1
```

## Where to start editing
- CMS layout: `app/templates/cms/base_cms.html`, `app/templates/cms/nav.html`, `app/static/cms/cms.css`
- Public layout: `app/templates/base_public.html`, public themes under `app/static/publicthemes/themes/`
- Each module’s templates under `app/templates/<module>/` and views in `app/<module>/views.py`
