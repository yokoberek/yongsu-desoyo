# Development

Technical guide for working on the Kampung Yongsu Desoyo site.

## Stack

- Python 3.13+, Django 6
- uv for dependencies (`pyproject.toml` + `uv.lock`)
- python-decouple for configuration (`.env`)
- django-tailwind (Tailwind CSS v4), theme in `theme/`
- Alpine.js (CDN) for interactivity
- django-unfold admin at `/site-manager/`
- WhiteNoise for static files
- django-debug-toolbar and django-browser-reload in development

## Requirements

- Python 3.13+
- uv — https://docs.astral.sh/uv/
- Node.js and npm (to build the Tailwind theme)

## Setup

```bash
git clone git@github.com:yokoberek/yongsu-desoyo.git
cd yongsu-desoyo

uv sync                                  # create .venv and install dependencies
cp .env.example .env                     # then set SECRET_KEY, DEBUG, ALLOWED_HOSTS

uv run python manage.py migrate
uv run python manage.py tailwind install # install the theme's npm packages
uv run python manage.py tailwind build   # compile CSS
uv run python manage.py runserver
```

The site runs at http://127.0.0.1:8000. Create an admin user with
`uv run python manage.py createsuperuser` and sign in at `/site-manager/`.

`manage.py` reads `DJANGO_SETTINGS_MODULE` from `.env`, so `.env` must exist before running
any management command. It defaults to `django_project.settings.development`.

## Environment

Configuration is read from `.env` via python-decouple; see `.env.example` for the full list.
Development uses SQLite and needs only `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`. Production
adds the PostgreSQL and email variables.

Settings are split:

- `django_project/settings/base.py` — shared settings, installed apps, templates, static
- `django_project/settings/development.py` — SQLite, debug toolbar, browser reload
- `django_project/settings/production.py` — PostgreSQL, SSL/HSTS/secure cookies, SMTP email

## Tailwind workflow

The palette, fonts, and custom CSS live in `theme/static_src/src/styles.css` inside a
Tailwind v4 `@theme` block — not in a CDN config. The base template loads the compiled file
with `{% tailwind_css %}`.

```bash
uv run python manage.py tailwind start   # watch and rebuild during development
uv run python manage.py tailwind build   # one-off production build
```

The compiled output (`theme/static/css/dist/styles.css`) is git-ignored and must be built in
each environment.

## Project structure

```
django_project/   settings (base/development/production), urls, wsgi/asgi
templates/        base layout and shared partials
  main_layout.html
  partials/       navbar.html, footer.html, page_banner.html
theme/            django-tailwind app; source CSS in static_src/src/styles.css
commons/          home, about, contact, statistics
tourism/ products/ culture/         potential domain
news/ events/ gallery/              information domain
development/                        village projects
ppid/                               public-information module
manage.py  pyproject.toml  uv.lock  .env.example
```

## Apps and routes

Each domain is a separate app. Public URLs are Indonesian; app, view, template, and reverse
names are English.

| App | View(s) | Template | Route |
|-----|---------|----------|-------|
| commons | HomeView, AboutView, ContactView, StatisticsView | `commons/*.html` | `/`, `/tentang/`, `/kontak/`, `/statistik/` |
| tourism | DestinationListView | `tourism/destination_list.html` | `/wisata/` |
| products | ProductListView | `products/product_list.html` | `/produk/` |
| culture | TraditionListView | `culture/tradition_list.html` | `/budaya/` |
| news | PostListView | `news/post_list.html` | `/berita/` |
| events | EventListView | `events/event_list.html` | `/acara/` |
| gallery | PhotoListView | `gallery/photo_list.html` | `/galeri/` |
| development | ProjectListView | `development/project_list.html` | `/pembangunan/` |
| ppid | PpidHomeView, ProfileView, PublicInformationView, InformationRequestView, FaqView | `ppid/*.html` | `/ppid/...` |

Apps are mounted in `django_project/urls.py`; catalog apps keep their Indonesian path segment
in their own `urls.py`, and PPID is nested under `/ppid/`.

## Conventions

- One app per domain entity. Do not group unrelated entities under one app because they share
  a navbar dropdown.
- Code is English (app, view, `app_name`, url reverse names, template filenames). Public URL
  paths and page content stay Indonesian.
- Templates follow Django naming: `<model>_list.html`, later `<model>_detail.html`.
- Link with `{% url %}` and namespaces; never hardcode paths.
- Reuse the shared partials (`page_banner.html`, `navbar`, `footer`, `ppid/_subnav.html`)
  instead of duplicating markup.
- Comments are short and factual — a section label, or a non-obvious "why" (a placeholder to
  replace, an Alpine plugin load order). No decorative banners or comments that restate markup.
- Use canonical Tailwind v4 classes (`opacity-6`, `aspect-4/5`, `bg-linear-to-t`), not
  arbitrary `[...]` values when a canonical exists.

## Adding a new app

```bash
uv run python manage.py startapp <name>
```

1. Register it in `INSTALLED_APPS` as `"<name>.apps.<Name>Config"`.
2. Add `views.py` (a `TemplateView`, or a `ListView`/`DetailView` once models exist).
3. Add `urls.py` with `app_name = "<name>"` and an Indonesian path.
4. Include it in `django_project/urls.py`.
5. Add templates under `<name>/templates/<name>/` using the `<model>_list.html` convention.
6. Extend `main_layout.html` and reuse `partials/page_banner.html`.

## Verifying changes

Run the system check, then load the affected routes and confirm real content renders (not
only that the process starts):

```bash
uv run python manage.py check
uv run python manage.py runserver
# in another shell:
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/wisata/
```

## Production

Set `DJANGO_SETTINGS_MODULE=django_project.settings.production` and provide the PostgreSQL and
security variables from `.env.example`, then:

```bash
uv run python manage.py tailwind build
uv run python manage.py collectstatic --noinput
uv run python manage.py migrate
```

Production enables SSL redirect, HSTS, and secure cookies, and serves static files via
WhiteNoise. Serve with a WSGI server such as gunicorn (`django_project.wsgi`).

## Commits

Group commits by context (infrastructure, theme, layout, then per app or per domain). Keep
subjects in the conventional style already used in the history, for example:

```
feat(ppid): add public information transparency module
```
