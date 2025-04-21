from argon2 import PasswordHasher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app_sql.db.models import Base, Employer, Job, User, JobApplication
from app_sql.settings.config import DB_URL
from app_sql.db.data import jobs_data,employers_data, users_data, applications_data

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
ph = PasswordHasher()

def prepare_database():
    from app_sql.utils import hash_password
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    sess_invoke = Session()
    
    for employer in employers_data:
        #create a new instance of employer, add it to session
        # Employer(id = employer.get('id'),.....)
        # ** unpack dictionary
        emp = Employer(**employer)
        sess_invoke.add(emp)

    for job in jobs_data:
        job = Job(**job)
        sess_invoke.add(job)

    for user in users_data:
        #user['password_hash'] = ph.hash(user['password'])
        user['password_hash'] = hash_password(user['password'])
        del user['password']
        user = User(**user)
        sess_invoke.add(user)

    for app in applications_data:
        application = JobApplication(**app)
        sess_invoke.add(application)

    sess_invoke.commit()
    sess_invoke.close()