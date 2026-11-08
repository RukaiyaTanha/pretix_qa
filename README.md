# Pretix QA Automation

A UI test automation project for [Pretix](https://pretix.eu/), built with Python, Selenium WebDriver and Pytest. The project focuses on testing the product category, product and quota management features of the Pretix event ticketing platform.

The automation suite uses the Page Object Model (POM) to keep test logic and page interactions separate.

## Tech Stack

- Python 3.14
- Selenium WebDriver
- Pytest
- pytest-html
- Google Chrome
- Jenkins
- Git and GitHub

## Features Tested

### 1. Product Category Management

- Open product categories page
- Create a category with valid information
- Validate an empty category name
- Edit an existing category name
- Change category type
- Delete an unused category

### 2. Product Management

- Open product list
- Create a product with valid information
- Validate an empty product name
- Validate negative product price
- Edit product name
- Edit product price
- Add product description
- Create products with duplicate names
- Delete an unused product

### 3. Quota Management

- Open quota management page
- Create a quota with valid capacity
- Create a quota with zero capacity
- Assign an additional product to an existing quota
- Change quota capacity

## Local Setup

### Prerequisites

- Python 3.14 or compatible version
- Google Chrome
- Git
- A running local Pretix application

### 1. Clone the repository

```bash
git clone https://github.com/RukaiyaTanha/pretix_qa.git
cd pretix_qa
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Set your Pretix administrator credentials in PowerShell:

```powershell
$env:ADMIN_EMAIL="your-admin-email"
$env:ADMIN_PASSWORD="your-admin-password"
```

The test configuration reads these values through environment variables. Do not commit actual credentials to GitHub.

### 5. Run the tests

Run the complete suite:

```powershell
pytest tests/ -v -s
```

Generate an HTML report:

```powershell
pytest tests/ -v -s --html=report.html --self-contained-html
```

Open `report.html` in a browser to review the execution results.

## Jenkins CI Pipeline

The project includes a `Jenkinsfile` for automated test execution.

The pipeline performs these steps:

1. Checks the execution environment.
2. Checks whether the local Pretix application is reachable.
3. Creates a Python virtual environment.
4. Installs project dependencies.
5. Retrieves Pretix admin credentials from Jenkins Credentials.
6. Executes the Selenium test suite.
7. Archives the generated HTML test report.

### Jenkins Credentials

Create a Jenkins credential with the following ID:

```text
pretix-admin-credentials
```

Use the **Username with password** credential type.

The Jenkinsfile passes the credentials as:

```text
ADMIN_EMAIL
ADMIN_PASSWORD
```

Actual credentials must remain outside the repository.

### Pipeline Execution

The Jenkins job uses:

- Definition: Pipeline script from SCM
- SCM: Git
- Repository: `https://github.com/RukaiyaTanha/pretix_qa.git`
- Branch: `main`
- Script Path: `Jenkinsfile`

The HTML report is available under the build's **Build Artifacts** section.

## Current Test Execution Results

Latest recorded execution:

| Result | Count |
|---|---:|
| Passed | 19 |
| Failed | 1 |
| Total | 20 |

### Known Application Defect

**Negative Product Price Validation**

The negative-price test found that Pretix accepted and saved a product with a negative price instead of rejecting the value.

This is recorded as an application defect. The failed test is intentionally retained so that the issue remains visible during regression execution.


