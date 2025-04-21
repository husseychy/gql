# filepath: /home/hussey/Projects/All_Usecase/graphql/app_sql/db/gql_queries.py
from graphene import Schema, ObjectType,String, Int, List, Field
from app_sql.gql.gql_types import JobObject, EmployerObject, UserObject, JobApplicationObject
from app_sql.db.database import Session
from app_sql.db.models import Job, Employer, User, JobApplication

class Query(ObjectType):
    jobs = List(JobObject)
    # get job by id 
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    users = List(UserObject)
    job_applications = List(JobApplicationObject)

    @staticmethod
    def resolve_job_applications(root, info):
        return Session().query(JobApplication).all()
    '''
query{
  jobApplications{
    id
    userId
    jobId
    user{
      username
      email
      role
    }
    job{
      title
      description
    }
  }
}
    '''

    @staticmethod
    def resolve_users(root, info):
        return Session().query(User).all()
    '''
query{
  users{
    username
    id
    email
    role
  }
}    
    '''

    @staticmethod #find based on id
    def resolve_employer(root, info, id):
        return Session().query(Employer).filter(Employer.id == id).first()
    # Created fragments to get the details as below
    
    '''
query{
  employer (id : 2){
    ...employerFields
  }
}

fragment employerFields on EmployerObject{
  id name contactEmail industry jobs{
    ...jobFields
  }
}

fragment jobFields on JobObject{
  id title description employerId
}
    '''

    @staticmethod #find based on id
    def resolve_job(root, info, id):
        return Session().query(Job).filter(Job.id == id).first()

    '''
    def resolve_job(root, info, id):
        session = Session()
        job = session.query(Job).filter(Job.id == id).first()
        session.close()
        return job
    '''
    '''
query{
  job(id:1){
    id
    description
    employer{
      id
      industry
    }
  }
}
    '''

    @staticmethod #this is because it is for graphene not related to cls
    def resolve_jobs(root, info):
        return Session().query(Job).all()
    # dependencies are working in the types return root.employer - working now
    # return Session().query(Job).options(joinedload(Job.employer)).all()
    # above is required if it was not working
    # import sqlalchemy.orm import joinedload
    
    @staticmethod #this is because it is for graphene not related to cls
    def resolve_employers(root, info):
        return Session().query(Employer).all()