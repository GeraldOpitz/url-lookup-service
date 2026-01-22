# URL Lookup Service

A simple HTTP service that determines whether a given URL is considered malicious.
It is designed to be queried by an HTTP proxy before allowing outbound connections.

This project was intentionally built with a simple initial implementation and can
be extended to handle larger scale and more complex requirements.

---

## Requirements

- Python 3.10 or newer
- macOS or Linux

---

## Project Structure

```bash
├── app/ # Application source code
├── tests/ # Automated tests
├── bad_urls.txt # Sample malicious URLs
├── requirements.txt
└── README.md
```
---

## Setup

Clone the repository:

```bash
git clone https://github.com/GeraldOpitz/url-lookup-service
cd url-lookup-service
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies:

```bash
pip install -r requirements.txt
```
---

## Running the service

Start the web server locally:

```bash
uvicorn app.main:app --reload
```

The service will be available at:

```bash
http://127.0.0.1:8000
```
---

## API Usage

Check URL safety

Request
```bash
GET /urlinfo/1/{hostname_and_port}/{path_and_query}
```
Example (safe URL)
```bash
GET /urlinfo/1/www.google.com/search?q=test
```

Response
```bash
{
  "url": "www.bad.com/malware",
  "safe": false,
  "reason": "URL found in malware database"
}
```

---

## Running tests

To run the test suite:

```bash
pytest
```
To run tests with coverage:

```bash
pytest -v --cov=app
```

---

## Development Workflow

The project was developed incrementally using small, focused commits.
Each commit introduces a single concern (project structure, endpoint,
business logic, tests, documentation) to make the development process
easy to follow and review.
