# Kneipe OS

**Everything you need to run your place. No bullshit.**

[![CI](https://github.com/LemuelCushing/el0lobo_cms_let_claude_loose/actions/workflows/ci.yml/badge.svg)](https://github.com/LemuelCushing/el0lobo_cms_let_claude_loose/actions/workflows/ci.yml)

Kneipe OS is a venue management system for collectives and other folk who actually work and run venues. Public website, event calendar, staff scheduling, point of sale, inventory tracking, and internal comms - all in one Django app. 
Built by folks who know that running a space means you mostly don't know where most of your shit is and that keeping records across teams is a nightmare.

This fixes that.

---

## Get Running

```bash
./bin/setup
./bin/dev
```

Open **http://127.0.0.1:8000** — log in with `admin` / `admin123` (Or, force login coz you're in dev)

> **Windows?** `python bin\setup` and `python bin\dev`

You're done. You're running a complete venue management system.

---

## What's Inside

### Public-Facing
- **Event calendar** — recurring events, one-offs, the whole deal
- **Customizable themes** — make it yours
- **Page builder** — CMS that doesn't suck
- **Artist profiles** — bands, DJs, whoever

### Staff Tools
- **Shift scheduling** — templates, assignments, the boring stuff automated
- **Point of sale** — multi-payment, discounts, actually usable
- **Inventory** — bar stock, merch, know what you have
- **Internal comms** — messages, email, all in one place
- **Asset manager** — photos, videos, documents organized
- **Venue maps** — floorplans for when people ask "where's the bathroom?"

### Tech That Works
- **Django 5.2** — because it's 2025 and PHP is dead
- **PostgreSQL or SQLite** — your call
- **HTMX** — dynamic UI without webpack hell
- **REST API** — Django REST Framework
- **Background jobs** — Celery + Redis for the slow stuff

---

## Daily Commands

```bash
./bin/dev              # Start the server
./bin/update           # Pull changes, update dependencies, run migrations
./bin/test             # Run tests
./bin/console          # Django shell (shell_plus if you have it)
./bin/manage migrate   # Migrations
```

### Before Committing
```bash
./bin/format           # Auto-format (black + ruff)
./bin/check            # Lint, types, the works
```

## Where to start editing
- CMS layout: `app/templates/cms/base_cms.html`, `app/templates/cms/nav.html`, `app/static/cms/cms.css`
- Public layout: `app/templates/base_public.html`, public themes under `app/static/publicthemes/themes/`
- Each module’s templates under `app/templates/<module>/` and views in `app/<module>/views.py`

## License

[add license here]
