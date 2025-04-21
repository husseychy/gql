# filepath: /home/hussey/Projects/All_Usecase/graphql/app_sql/db/data.py

employers_data = [
    {"name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"title": "Accountant III", "description": "Manage financial records", "employer_id": 2},
    {"title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]

users_data = [
    {"username": "hussey", "email": "hussey@gmail.com", "password": "h123", "role": "admin"},
    {"username": "shaz", "email": "shaz@gmail.com", "password": "s123", "role": "user"},
    {"username": "alice", "email": "alice@gmail.com", "password": "a123", "role": "user"},
]

applications_data = [
    {"user_id": 2, "job_id": 1},
    {"user_id": 2, "job_id": 2},
    {"user_id": 1, "job_id": 2},
    {"user_id": 2, "job_id": 4}
]

'''

employers_data = [
    {"id": 1, "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"id": 2, "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"id": 3, "title": "Accountant III", "description": "Manage financial records", "employer_id": 2},
    {"id": 4, "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]

'''