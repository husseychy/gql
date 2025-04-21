# filepath: /home/hussey/Projects/All_Usecase/graphql/app_sql/main.py
from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
from app_sql.db.database import prepare_database, Session
from app_sql.db.models import Employer, Job
from app_sql.gql.gql_queries import Query
from app_sql.gql.gql_mutations import Mutation
    
schema = Schema(query= Query, mutation=Mutation)

app = FastAPI()

@app.on_event('startup')
def startup_event():
    prepare_database()

@app.get('/employers')
def get_employers():
    get_emp_sess = Session()
    employers = get_emp_sess.query(Employer).all()
    get_emp_sess.close()
    return employers
#http://127.0.0.1:8000/employers

@app.get('/jobs')
def get_jobs():
    with Session() as session:
        return session.query(Job).all()

#app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))

# Graphql don't support dynamic header hence you need to pass via postman or manually here for tesing

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))
# Use http://127.0.0.1:8000/graphql/

#app.mount("/graphql-p", GraphQLApp(schema=schema, on_get=make_graphiql_handler()))

# uvicorn app_sql.main:app --reload
# Below is the gql query
# sudo lsof -i :8000 - List of task running
# sudo kill -9 402
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