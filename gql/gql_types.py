from graphene import Schema, ObjectType,String, Int, List, Field

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)  #CLASS INITIATION ISSUE HENCE CREATED LAMBDA

    @staticmethod
    def resolve_jobs(root, info):
        return root.jobs

class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = String()
    employer = Field(lambda: EmployerObject)
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        return root.applications
    
    '''
query{
  job (id:2){
    title
    description
    employer{
      name
      contactEmail
    }
    applications{
      userId
    }
  }
}
    '''

    @staticmethod
    def resolve_employer(root, info):
        # iterate over employer and break
        # list comprension, we need only single employer
        return root.employer
    
class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_applications(root, info):
        return root.applications
    '''
query{
  users{
    id
    username
    email
    role
    applications{
      jobId
    }
  }
}
    '''

class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda: UserObject)
    job = Field(lambda: JobObject)

    @staticmethod
    def resolve_user(root, info):
        return root.user
    
    @staticmethod
    def resolve_job(root, info):
        return root.job