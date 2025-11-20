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

### Before Pushing
```bash
./bin/ci               # Full CI suite locally—catch it before GitHub does
```

---

## Structure

```
app/
├── events/      # Events, recurring stuff, tickets
├── shifts/      # Staff scheduling
├── pos/         # Point of sale
├── menu/        # Food and drinks
├── merch/       # Merch catalog
├── inventory/   # Stock tracking
├── bands/       # Artists/performers
├── comms/       # Messaging + email
├── assets/      # File manager
├── pages/       # CMS pages
├── cms/         # Dashboard
├── users/       # Profiles, perms
└── setup/       # Settings
```

---

## Common Tasks

### Add a Feature
```bash
./bin/manage startapp yourfeature
# Edit models, views, whatever
./bin/manage makemigrations
./bin/manage migrate
./bin/test
```

### Deploy
```bash
docker compose up --build
```

---

## Config

Bar OS uses environment variables. Copy `.env.sample` to `.env`:

```env
DJANGO_ENV=[development|staging|production]
DEBUG=True
SECRET_KEY=change-this-in-production
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Docs

- **[Development Guide](DEVELOPMENT.md)** — Testing, code quality, deep dives
- **[Architecture](ARCHITECTURE.md)** — How it's built
- **[Contributing](CONTRIBUTING.md)** — Join in
- **[Security](SECURITY_AUDIT_REPORT.md)** — Don't get hacked
- **[Coding Conventions](CODING_CONVENTIONS.md)** — Code style
- **[bin/ Scripts](bin/README.md)** — Tool docs

---

## Requirements

- **Python 3.11+** (3.11, 3.12, 3.13 all work)
- **Git**
- **Docker** (optional, for PostgreSQL)

---

## Platform Notes

Scripts work everywhere. Same commands, same results.

**Unix/Mac:**
```bash
./bin/setup
./bin/dev
```

**Windows:**
```cmd
python bin\setup
python bin\dev
```

---

## Help

- `./bin/manage --help` — Django commands
- `make help` — Quick ref (Unix/Mac)

## License

[Your license here]
