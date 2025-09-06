# ACEest Fitness - DevOps Assignment

This repository contains a simple **fitness and gym management system** application with a `Tkinter` GUI in Python.  
It is integrated with **Pytest** for unit testing and a **GitHub Actions pipeline** for continuous integration.  
The project demonstrates key DevOps practices such as version control, automated testing, and CI/CD.

---

## Features

- Log workouts with name and duration.
- View logged workouts.
- Input validation for incorrect or empty fields.
- Fully tested with **Pytest** (GUI interactions mocked).
- Automated pipeline using **GitHub Actions**.

---

## Local Setup

### Prerequisites

- Python **3.12** (or compatible version)
- Git

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/ShivomA/aceest-fitness-gym-devops.git
cd aceest-fitness-gym-devops
```

Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

Install all requirements

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the Application

```bash
python ACEest_Fitness.py
```

### Run Tests Locally

```bash
pytest -v
```

### Running with Docker

Build the Docker image

```bash
docker build -t aceest_fitness .
```

Run the application

```bash
docker run --rm aceest_fitness
```

## GitHub Actions CI/CD Pipeline

The repository includes a **GitHub Actions workflow** (`.github/workflows/ci.yml`) that runs automatically on every push
or pull request to the `main` branch.

### Pipeline Steps

1. **Checkout code** – Fetch the repository contents.
2. **Set up Python** – Install Python 3.12 on the GitHub Actions runner.
3. **Install dependencies** – Upgrade pip and install from `requirements.txt`.
4. **Run tests** – Execute Pytest to validate application functionality.  
