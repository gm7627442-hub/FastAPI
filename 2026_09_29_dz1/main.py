from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Homework App")


class UserIn(BaseModel):
    name: str
    age: int


class UserOut(UserIn):
    is_adult: bool


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.get("/square/{number}")
def square(number: int):
    return {"number": number, "square": number ** 2}


@app.get("/fullname")
def fullname(name: str, surname: str):
    return {"fullname": f"{name} {surname}"}


@app.post("/user", response_model=UserOut)
def create_user(user: UserIn):
    return UserOut(
        name=user.name,
        age=user.age,
        is_adult=user.age >= 18,
    )


@app.get("/reverse/{text}")
def reverse(text: str):
    return {"original": text, "reversed": text[::-1]}