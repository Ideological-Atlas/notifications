# Ideological Atlas - Notifications Microservice

![CI](https://github.com/Ideological-Atlas/notifications/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Ideological-Atlas/notifications/graph/badge.svg?token=W9D4BVTK2Y)](https://codecov.io/gh/Ideological-Atlas/notifications)
![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688.svg)
![License](https://img.shields.io/badge/license-GPLv3-green)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![gitleaks](https://img.shields.io/badge/protected%20by-gitleaks-blueviolet)](https://github.com/gitleaks/gitleaks)
[![shellcheck](https://img.shields.io/badge/shellcheck-enforced-4EAA25)](https://github.com/koalaman/shellcheck)
[![codespell](https://img.shields.io/badge/spell%20check-codespell-blue)](https://github.com/codespell-project/codespell)

A high-performance, asynchronous microservice designed to handle transactional emails for the **Ideological Atlas** platform. Built with **FastAPI** and **Python 3.14**, it leverages **Resend** for email delivery, **Jinja2** for dynamic HTML templating, and full internationalization (i18n) support.

## 🚀 Features

* **REST API:** Clean and documented endpoints to trigger email dispatch.
* **Email Provider:** Integrated with [Resend](https://resend.com/) for reliable delivery.
* **Templating Engine:** Uses Jinja2 with inheritance support (`base.html`) for consistent email branding.
* **Internationalization:** Built-in support for multiple languages via JSON locale files.
* **Security:** API Key authentication using HTTP Headers.
* **Modern Stack:** Python 3.14, FastAPI, `uv` package manager, and Pydantic v2.
* **DevOps Ready:** Dockerized, comprehensive `Makefile`, and CI/CD pipelines with GitHub Actions.
* **Code Quality:** Strict linting (Ruff, Black, Isort, Mypy) and high test coverage.

## 🛠 Tech Stack

* **Language:** Python 3.14
* **Framework:** FastAPI
* **Server:** Uvicorn
* **Dependency Management:** uv
* **Containerization:** Docker & Docker Compose
* **Testing:** Unittest & Coverage
* **CI/CD:** GitHub Actions

## 📂 Project Structure

```text
.
├── .github/workflows   # CI/CD pipelines
├── docker              # Docker configuration files
├── src
│   ├── app
│   │   ├── core        # Configuration, Security, Logging
│   │   ├── locales     # JSON translation files
│   │   ├── routers     # API Endpoints
│   │   ├── schemas     # Pydantic models
│   │   └── services    # Business logic (Email Engine)
│   ├── templates       # Jinja2 HTML templates
│   ├── tests           # Unit tests
│   └── main.py         # Application entry point
├── compose.yml         # Docker Compose services
├── Makefile            # Task automation
└── pyproject.toml      # Project dependencies and tool config

```

## ⚡ Getting Started

### Prerequisites

* **Docker** and **Docker Compose** (Recommended for development)
* **Python 3.14+** and **uv** (If running locally without Docker)

### Environment Configuration

1. Copy the example environment file:
```bash
cp .env-dist .env

```


2. Configure the variables in `.env`:

| Variable | Description | Default |
| --- | --- | --- |
| `PROJECT_NAME` | Name of the project | `ideologicalatlas` |
| `RESEND_API_KEY` | **Required**. Your Resend API Key | `CHANGE-ME` |
| `API_KEY` | **Required**. Secret key to protect the API | `CHANGE-ME` |
| `PORT` | Service port | `5051` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `FROM_EMAIL` | Sender email address | `noreply@...` |
| `BASE_BACKEND_URL` | URL for link generation | `localhost` |

## 🐳 Docker Usage (Recommended)

This project includes a robust `Makefile` to simplify Docker operations.

1. **Start the service:**
```bash
make up

```


This creates the `.env` file (if missing), builds the image, and starts the container in the background.
2. **View Logs:**
```bash
make logs

```


3. **Stop the service:**
```bash
make down

```


4. **Rebuild completely:**
```bash
make complete-build

```



## 💻 Local Development

If you prefer running without Docker:

1. **Install `uv`:**
```bash
pip install uv

```


2. **Install dependencies:**
```bash
cd src
uv sync --extra dev

```


3. **Run the application:**
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 5051 --reload

```



## 📡 API Usage

### Send Email Endpoint

* **URL:** `/notifications/send`
* **Method:** `POST`
* **Auth:** Header `x-api-key: <YOUR_API_KEY>`

#### Request Body

```json
{
  "to_email": "user@example.com",
  "template_name": "register",
  "language": "es",
  "context": {
    "user_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Jane Doe"
  }
}

```

#### Example cURL

You can use the built-in make command to trigger a test email:

```bash
make trigger-test

```

Or manually:

```bash
curl -X POST http://localhost:5051/notifications/send \
   -H "Content-Type: application/json" \
   -H "x-api-key: YOUR_SECRET_KEY" \
   -d '{"to_email": "test@test.com", "template_name": "register", "language": "en", "context": {"user_uuid": "123"}}'

```

## 🧪 Testing & Quality

We maintain high code quality standards enforced by **Pre-commit** hooks and **Unittest**.

### Running Tests

To run the test suite with coverage inside the Docker container:

```bash
make test

```

### Static Analysis

Linting and formatting are handled by `ruff`, `black`, and `isort`. You can run the pre-commit checks manually:

```bash
# Ensure dev dependencies are installed
uv run pre-commit run --all-files --config .pre-commit-config.yaml

```

## 📝 License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
