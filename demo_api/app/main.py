from fastapi import FastAPI, HTTPException, status
import sqlite3
import hashlib
from pydantic import BaseModel

app = FastAPI()

DB_PATH = "demo.db"

class User(BaseModel):
    Login: str
    Password: str
    Name: str

class Task(BaseModel):
    Description: str
    Status: str
    Priority: int
    UserId: int


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS USER (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Login TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL,
            Name TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TASK (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Description TEXT NOT NULL,
            Status TEXT NOT NULL,
            Priority INTEGER NOT NULL,
            UserId INTEGER NOT NULL,
            FOREIGN KEY (UserId) REFERENCES USER (Id)
        )
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()


def hash_password(password: str) -> str:
    return hashlib.sha512(password.encode()).hexdigest()

@app.get("/")
def root():
    return {"Bienvenue sur l'API Demo"}

@app.get("/user")
def get_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER")
    users = cursor.fetchall()
    conn.close()
    return users

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO USER (Login, Password, Name) VALUES (?, ?, ?)",
            (user.Login, hash_password(user.Password), user.Name)
        )
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Le nom d'utilisateur existe déjà")
    conn.close()
    return {"id": user_id}

@app.get("/user/{id}")
def get_user(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER WHERE Id = ?", (id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="L'utilisateur n'existe pas")
    return user

@app.put("/user/{id}")
def update_user(id: int, user: User):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE USER SET Login = ?, Password = ?, Name = ? WHERE Id = ?",
        (user.Login, hash_password(user.Password), user.Name, id)
    )
    conn.commit()
    conn.close()
    return {"Utilisateur mis à jour"}

@app.delete("/user/{id}")
def delete_user(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM USER WHERE Id = ?", (id,))
    conn.commit()
    conn.close()
    return {"L''utilisateur a été supprimé"}


@app.get("/task")
def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TASK")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

@app.post("/task", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO TASK (Description, Status, Priority, UserId) VALUES (?, ?, ?, ?)",
        (task.Description, task.Status, task.Priority, task.UserId)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {"id": task_id}

@app.get("/task/{id}")
def get_task(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TASK WHERE Id = ?", (id,))
    task = cursor.fetchone()
    conn.close()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche pas trouvée")
    return task

@app.put("/task/{id}")
def update_task(id: int, task: Task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE TASK SET Description = ?, Status = ?, Priority = ?, UserId = ? WHERE Id = ?",
        (task.Description, task.Status, task.Priority, task.UserId, id)
    )
    conn.commit()
    conn.close()
    return {"Tâche mise à jour"}

@app.delete("/task/{id}")
def delete_task(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TASK WHERE Id = ?", (id,))
    conn.commit()
    conn.close()
    return {"Tâche supprimée"}
