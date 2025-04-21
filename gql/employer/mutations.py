from graphene import String, Int, Field, List, Mutation, ObjectType,Boolean
from app_sql.gql.gql_types import JobObject, EmployerObject
from app_sql.db.database import Session
from app_sql.db.models import Employer
from sqlalchemy.orm import joinedload
from app_sql.db.models import Employer, User
from app_sql.utils import get_authenticated_user, admin_user

                    
class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda : EmployerObject)

    #v1 - used as draft
    #authenticated_as = Field(String)

    # @static is not needed explicitly we are adding decorator
    # to check admin user before we give the permission

    @admin_user
    def mutate(root, info, name, contact_email, industry):
        #v1 - used as draft
        #user = get_authenticated_user(info.context)

        session = Session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer) #we have not provided id , it will be taken care by Postgres
        #return AddEmployer(employer=employer)

        #temp
        #v1 - used as draft return AddEmployer(employer=employer, authenticated_as=user.email)
        return AddEmployer(employer=employer)
    
class UpdateEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda : EmployerObject)

    @admin_user
    def mutate(root, info, employer_id, name=None, contact_email=None, industry=None):
        session = Session()
        employer = session.query(Employer).filter(Employer.id == employer_id).first()
        
        if not employer:
            raise Exception('employer not present')
        
        #job = Job(name=name, contact_email=contact_email, industry=industry)

        if name is not None:
            employer.name = name
        if contact_email is not None:
            employer.contact_email = contact_email
        if industry is not None:
            employer.industry = industry

        session.commit()
        session.refresh(employer) #we have not provided id , it will be taken care by Postgres
        session.close()
        return UpdateEmployer(employer=employer)
    
class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @admin_user
    def mutate(root, info, id):
        session = Session()
        employer = session.query(Employer).filter(Employer.id == id).first()
        # In the models.py we have set a new attribute lazy to deal with it, but can cause  performance challenges if we have big tables relationship
        if not employer:
            raise Exception('Employer not present')
        
        session.delete(employer)
        session.commit()
        session.close()
        return DeleteEmployer(success=True)
'''
---------------------------EMPLOYER----------------------------------
mutation {
  addEmployer(name: "Some name", 
    contactEmail: "Some email", 
    industry: "some ind") {
    employer {
      name
      industry
    }
  }
}
'''
'''
mutation {
  updateEmployer(
    employerId: 1
    name: "updated name"
    contactEmail: "new email"
    industry: "updated ind"
  ) {
    employer {
      ...employerFields
    }
  }
}

fragment employerFields on EmployerObject {
  id
  name
  contactEmail
  industry
  jobs {
    ...jobFields
  }
}

fragment jobFields on JobObject {
  id
  title
  description
  employerId
}

'''

'''
mutation{
  deleteEmployer(id: 2){
    success
  }
}
'''

'''
This is how payload looks like

HEADER:ALGORITHM & TOKEN TYPE

{
  "alg": "HS256",
  "typ": "JWT"
}
PAYLOAD:DATA
{
  "sub": "hussey@gmail.com",
  "exp": 1744997613
}
VERIFY SIGNATURE

HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  
job_board_app_secret!

) secret base64 encoded
'''
'''
mutation{
  loginUser(
    email: "hussey@gmail.com",
    password :"h123"
  ){
    token
  }
}


Authorization payload

mutation {
  addEmployer(name: "Some name", 
    contactEmail: "Some email", 
    industry: "some ind") {
    employer {
      name
      industry
      contactEmail
      id
    }
    authenticatedAs
  }
}

{
  "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJodXNzZXlAZ21haWwuY29tIiwiZXhwIjoxNzQ1MDQxMTIyfQ.NxuacbKIyxxPw3Fikr4N_h0IVXTIGegqVn8DXg5EUqs"
}

Do it via postman as grapql playground don't work
Response as below

{
    "data": {
        "addEmployer": {
            "employer": {
                "name": "Some name",
                "industry": "some ind",
                "contactEmail": "Some email",
                "id": 3
            },
            "authenticatedAs": "hussey@gmail.com"
        }
    }
}

'''