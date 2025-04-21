# App_SQL: GraphQL Job Board Application

This project is a GraphQL-based job board application built using **FastAPI**, **Graphene**, and **SQLAlchemy**. It provides APIs for managing employers, jobs, and user authentication. **Use POSTMAN tool once you start sending the header information**

---

## Features

- **GraphQL API**: Query and mutate data for jobs, employers, and users.
- **Authentication**: JWT-based authentication for secure access.
- **Database Integration**: PostgreSQL database with SQLAlchemy ORM.
- **Password Security**: Argon2 for secure password hashing.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/husseychy/gql.git
   cd gql/app_sql
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   Update the `DB_URL` in `settings/config.py` with your PostgreSQL instance:
   ```python
   DB_URL = 'postgresql+psycopg://<your_postgres_instance>'
   ```

5. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```

---

## Configuration

The application uses the following configuration settings, defined in `settings/config.py`:

```python
DB_URL = 'postgresql+psycopg://<your postgres instance name>'
SECRET_KEY = "job_board_app_secret!"  # Use your secret key
ALGORITHM = "HS256"                   # Use your algorithm
TOKEN_EXPIRATION_TIME_MINUTES = 15    # Token expiration time in minutes
```

You can update these values as per your requirements.

---

## Endpoints

- **GraphQL Endpoint**: [http://127.0.0.1:8000/graphql](http://127.0.0.1:8000/graphql)

---

## Environment Variables

- `DB_URL`:SQL database connection string.
- `SECRET_KEY`: Secret key for JWT token generation.
- `ALGORITHM`: Algorithm used for JWT encoding/decoding.
- `TOKEN_EXPIRATION_TIME_MINUTES`: Token expiration time in minutes.

---

## Project Structure

```
app_sql/
├── db/
│   ├── data.py          # Sample data for jobs and employers
│   ├── database.py      # Database setup and session management
│   ├── models.py        # SQLAlchemy models
├── gql/
│   ├── gql_queries.py   # GraphQL queries
│   ├── gql_mutations.py # GraphQL mutations
│   ├── employer/
│       ├── mutations.py # Employer-specific mutations
├── settings/
│   ├── config.py        # Configuration settings
├── utils.py             # Utility functions and decorators
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── .gitignore           # Git ignore rules
```

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.