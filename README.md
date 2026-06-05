# fitness_club_final  

A Django‑based web application for managing a fitness club – members, instructors, workout plans, and financial reports.

---  

## Overview  

`fitness_club_final` provides a complete back‑office system for a fitness club.  Administrators can:

* Register customers and instructors  
* Create, assign and delete workout plans  
* Track expenses, fees, salaries, and generate profit reports  
* Manage user profiles and authentication  

The project is packaged as a standard Django project (`fitnessclub`) with a single reusable app (`myapp`).  All database schema changes are captured in the migration files.

---  

## Features  

| Category | Description |
|----------|-------------|
| **Member Management** | CRUD for customers, instructors, and user profiles. |
| **Workout Plans** | Create, edit, assign, and delete workout plans per member. |
| **Financial Reporting** | Expenses, fees, salary, and profit reports generated from the database. |
| **Admin Interface** | Fully‑featured Django admin for quick data entry and overview. |
| **Data Backup** | `backup.json` contains a fixture that can be loaded to restore sample data. |
| **Documentation** | Project specifications are stored in `Fitness Club Management.docx`. |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.9+ |
| **Web Framework** | Django 4.x |
| **Database** | SQLite (default) – can be swapped for PostgreSQL, MySQL, etc. |
| **Front‑end** | Django templates (Bootstrap can be added by the user) |
| **Version Control** | Git |
| **Deployment** | WSGI/ASGI compatible servers (e.g., Gunicorn, Daphne) |

---  

## Installation  

> **Prerequisite:** Python 3.9 or newer and `git` installed on your machine.

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-username/fitness_club_final.git
cd fitness_club_final

# 2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install --upgrade pip
pip install -r requirements.txt   # (create this file if not present, e.g. Django)

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ (Optional) Load sample data
python manage.py loaddata backup.json
```

> **Note:** If a `requirements.txt` file is missing, you can generate one with `pip freeze > requirements.txt` after installing Django (`pip install Django`).

---  

## Usage  

```bash
# Start the development server
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.  

* **Admin site:** `http://127.0.0.1:8000/admin/` – create a superuser first:  

  ```bash
  python manage.py createsuperuser
  ```

* **Application URLs:** All functional views are defined in `myapp/urls.py` and included in the project’s root `urls.py`.

* **Running tests (if any):**  

  ```bash
  python manage.py test
  ```

* **Collect static files for production:**  

  ```bash
  python manage.py collectstatic
  ```

---  

## License  

This project is licensed under the **MIT License** – see the `LICENSE` file for details.  

---  

*Feel free to fork, contribute, or adapt the code for your own fitness‑club management needs!*