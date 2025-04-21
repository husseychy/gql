from graphene import String, Int, Field, List, Mutation, ObjectType,Boolean
from app_sql.gql.gql_types import JobObject, EmployerObject
from app_sql.db.database import Session
from app_sql.db.models import Job
from sqlalchemy.orm import joinedload
from app_sql.utils import admin_user

class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda : JobObject)

    @admin_user
    def mutate(root, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        session = Session()
        session.add(job)
        session.commit()
        session.refresh(job) #we have not provided id , it will be taken care by Postgres
        return AddJob(job=job)

class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda : JobObject)

    @admin_user
    def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        job = Job(title=title, description=description, employer_id=employer_id)
        session = Session()

        '''job = session.query(Job) \
            .options(joinedload(Job.employer)) \
            .filter(Job.id == job_id).first()'''

        job = session.query(Job).filter(Job.id == job_id).first()
        # In the models.py we have set a new attribute lazy to deal with it, but can cause  performance challenges if we have big tables relationship
        if not job:
            raise Exception('Job not present')
        
        if title is not None:
            job.title = title
        if description is not None:
            job.description = description
        if employer_id is not None:
            job.employer_id = employer_id

        session.commit()
        session.refresh(job) #we have not provided id , it will be taken care by Postgres
        session.close()
        return UpdateJob(job=job)
    
class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @admin_user
    def mutate(root, info, id):
        session = Session()
        job = session.query(Job).filter(Job.id == id).first()
        # In the models.py we have set a new attribute lazy to deal with it, but can cause  performance challenges if we have big tables relationship
        if not job:
            raise Exception('Job not present')
        
        session.delete(job)
        session.commit()
        session.close()
        return DeleteJob(success=True)
    
'''
{
  jobs {
    id
    employerId
    description
    employer {
      id
      industry
    }
  }
  employers {
    id
    industry
    name
    jobs {
      id
      description
    }
  }
}
'''
'''
mutation {
  addJob(title: "Some title", description: "Some desc", employerId: 1) {
    job {
      id
    }
  }
}
'''
'''
mutation{
  updateJob(
    jobId : 1,
    description : "new job description"
    title : "Updated title"
    employerId : 2
  ){
    job{
      id
      description
      title
    }
  }
}
'''
#instant visible in SQL server post update

#If you are calling below it will not work as you need employer attribute to be loaded (we can think of it as Lazy evolution)

#delete operation
'''
mutation{
  deleteJob(id: 2){
    success
  }
}
'''