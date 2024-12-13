from fastapi import FastAPI
from pydantic import BaseModel

from sql_generation import generate_sql
from mysql_operations import execute_query, login
from memory_cache import add_to_cache
from auto_suggestion import suggest
import asyncio

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:4200"  # Frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class QueryRequest(BaseModel):
    query: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/search")
async def search(request: QueryRequest):
    try:
        sql_query = generate_sql(request.query)
        print(sql_query)
        columns, rows = execute_query(sql_query)

        # Update cache asynchronously
        asyncio.create_task(add_to_cache(request.query))
        return {"columns": columns, "rows": rows}
    except Exception as e:
        return {"error": str(e)}


@app.get("/suggestion")
async def generate(word: str):
    return suggest(word)


@app.post("/login")
async def search(request: LoginRequest):
    is_success, row = login(request.email, request.password)
    if is_success:
        return {"success": True, "fullname": row[0]}
    return {"success": False, "fullname": None}
