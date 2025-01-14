
# Pipedrive API Test Suite

## Project Overview
This project is a test automation suite for verifying person's contact creation functionality of the Pipedrive API. 

The main goals of this project are:
- Ensuring that the Pipedrive API functions as expected.
- Providing easy-to-run automated tests.
- Facilitating CI/CD integration via GitHub Actions.

---

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.12 or higher.
- Docker (for containerized execution).

---

## Running with Docker

### 1. Build the Docker Image
```bash
docker build -t pipedrive-tests:latest .
```

### 2. Run Tests in Docker
Pass the API token to the container at runtime:
```bash
docker run --rm -e PIPEDRIVE_API_TOKEN=<your_api_token> pipedrive-tests:latest
```

---

## Running Locally

### 1. Clone the Repository
```bash
git clone https://github.com/at0m1x19/Pipedrive
cd pipedrive-tests
```

### 2. Install Dependencies
Set up a virtual environment and install the required Python libraries:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set Your API Token
Copy and rename `.env_template` to `.env`. Add your  Pipedrive API token to the file.

### 4. Run Tests
Execute the test suite using `pytest`:
```bash
pytest -v
```

---

## CI Integration
The project includes a GitHub Actions workflow for continuous integration. This workflow:
1. Runs on each push and pull request to the `master` branch.
2. Automatically installs dependencies.
3. Executes the test suite.
4. Stores the results for review.

---

## Project Structure
- **tests/**: Contains the test cases.
- **api/**: Includes the API client for interacting with Pipedrive.
- **requirements.txt**: Lists the Python dependencies.
- **Dockerfile**: Defines the containerized environment.
- **ci.yml**: GitHub Actions workflow for CI/CD.
- **.env_template**: Env file for keeping secret for a local run.

---

