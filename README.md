# Pretix QA Automation Framework

UI test automation for the admin panel of [Pretix](https://github.com/pretix/pretix), an open-source ticketing and event management platform. Built with Python, Selenium, and Pytest using the Page Object Model (POM), and integrated with a Jenkins pipeline.

## Latest Results

| Metric | Value |
|---|---|
| Test Duration | 5 min 46 sec |
| Test Framework | Pytest |
| UI Automation | Selenium WebDriver |
| CI/CD | Jenkins |
| Report | HTML test report |

The test suite covers product category management, product management, and quota management.

The HTML report is generated as `report.html` after each test run. Jenkins archives the report as a build artifact.

## What Is Tested

| Area | Scenarios |
|---|---|
| Product Categories | Open category page, create category, empty-name validation, edit category name, change category type, delete unused category |
| Products | Open product list, create product, missing-name validation, negative-price validation, edit product name, update product price, add product description, duplicate product name, delete unused product |
| Quotas | Open quota management page, create quota with valid capacity, create quota with zero capacity, assign an additional product to an existing quota, change quota capacity |

## Tech Stack

- Python 3.14
- Selenium WebDriver
- Pytest, pytest-html
- Page Object Model
- Jenkins
- Git, GitHub
- Chrome WebDriver

## Project Structure

```text
Pretix_QA/
│
├── config/              Configuration and environment settings
├── pages/               Page Object classes
├── tests/               UI automation test cases
├── screenshots/         Screenshots captured during test runs
├── .venv/               Python virtual environment (local only)
├── conftest.py          Pytest fixtures
├── pytest.ini           Pytest settings
├── Jenkinsfile          Jenkins pipeline
├── requirements.txt     Python dependencies
├── .gitignore           Git ignored files
└── README.md            Project documentation
```

## Getting Started

**Prerequisites:** Python 3.14, Google Chrome, Git, and a running Pretix instance with an admin account.

```bash
# 1. Clone the repository
git clone https://github.com/RukaiyaTanha/pretix_qa.git

# 2. Open the project folder
cd pretix_qa

# 3. Create a virtual environment
python -m venv .venv

# 4. Activate the environment (Windows)
.venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt
```

Configure the following environment variables before running the tests:

```text
ADMIN_EMAIL=your_admin_email
ADMIN_PASSWORD=your_admin_password
```

The application URL is configured in `config/config.py`.

Run all tests and generate an HTML report:

```bash
pytest tests/ -v -s --html=report.html --self-contained-html
```

Run a single test file:

```bash
pytest tests/test_file_name.py -v -s
```

## CI/CD

The `Jenkinsfile` defines the **Pretix-QA-Pipeline** job.

The pipeline:

1. Checks the Python and Git environments.
2. Checks whether the local Pretix application is reachable.
3. Creates the Python virtual environment if needed.
4. Installs project dependencies.
5. Runs the Selenium automation test suite.
6. Archives the generated HTML report as a Jenkins build artifact.

The project is maintained on GitHub, with Jenkins used to execute the UI automation suite.

## Known Application Issue

During negative testing, Pretix accepted a product with a negative price instead of rejecting the input. This was recorded as an application-side validation issue.
