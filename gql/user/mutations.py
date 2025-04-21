import string
from random import choices
from graphene import String, Int, Field, List, Mutation, ObjectType,Boolean
from graphql import GraphQLError
from app_sql.gql.gql_types import UserObject
from app_sql.db.database import Session
from app_sql.db.models import User, JobApplication
from app_sql.utils import verify_password, generate_token
from app_sql.gql.gql_types import UserObject, JobApplicationObject
from app_sql.utils import hash_password, get_authenticated_user,auth_user_same_as, auth_user

class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda : UserObject)

    @staticmethod
    def mutate(root, info, username, email, password, role):
        # if new user role is admin , only admin has right to add a admin user
        if role == 'admin':
            current_user = get_authenticated_user(info.context)
            if current_user.role != 'admin':
                raise GraphQLError('only admin has right to add a admin user')
        # Now we have to use this function at mutliple places
        # like user should be admin to add employer, job etc
        # we are using decorator to do this - take another fn
        # as input and extend the behaviour
        # input fn -> decorator -> output fn (modified)
        # layer of access control
        
        session = Session()

        user = session.query(User).filter(User.email == email).first()

        if user:
            raise GraphQLError('email exist')
        
        if not user:
        
          password_hash = hash_password(password)

          user = User(username=username, email=email, password_hash=password_hash, role=role)
          session.add(user)
          session.commit()
          session.refresh(user)
          return AddUser(user=user)
'''
mutation {
  addUser(
    username: "new user"
    email: "newemail@gmail.com"
    password: "n123"
    role: "user"
  ){
    user{
      id
      username
      email
      role
    }
  }
}
'''
# For admin add shaz user in loginuser gql , put the token in 
# authorization add above user with admin to check 

class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        
        user = session.query(User).filter(User.email == email).first()
        '''if not user or user.password != password:
            raise GraphQLError('Invalid email or password')
            token = ''.join(choices(string.ascii_lowercase, k=10))'''
        
        if not user:
            raise GraphQLError('Invalid email')
        
        '''ph = PasswordHasher()
        try:
            ph.verify(pwd_hash, pwd)
        except VerifyMismatchError:
            raise GraphQLError('Invalid password')'''
        
        #token = ''.join(choices(string.ascii_lowercase, k=10))
        verify_password(user.password_hash, password)

        token = generate_token(email)
        # go on jwt.io paste the token you will get header, payload and signature details
        # you will see signature error coz SECRET key is with us SECRET_KEY = "job_board_app_secret!"
        return LoginUser(token=token)
    
'''
mutation{
  loginUser(
    email: "hussey@gmail.com",
    password :"h123"
  ){
    token
  }
}
'''

class ApplyToJob(Mutation):
    class Arguments:
        user_id = Int(required=True)
        job_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject)

    #@auth_user # any user can apply to any job - you just need authentication
    @auth_user_same_as
    def mutate(root, info, user_id, job_id):
        session = Session()
        
        #check if user has already applied for the job
        existing_application = session.query(JobApplication).filter(
            JobApplication.user_id == user_id,
            JobApplication.job_id == job_id
            ).first()
        
        # we can think of adding a intergity issue in graphql and give composite 
        # key error as alternative approach 
        
        if existing_application:
            raise GraphQLError('User already applied for job')
        
        job_application = JobApplication(user_id=user_id, job_id=job_id)
        session.add(job_application)
        session.commit()
        session.refresh(job_application)

        return ApplyToJob(job_application=job_application)
    
'''
mutation{
  applyToJob(jobId : 1,
  userId : 1){
    jobApplication{
      id
      userId
      jobId
      user{
        username
        email
      }
      job{
        title
        description
        employer{
          name
          industry
        }
      }
    }
  }
}
'''