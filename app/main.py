from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from .config import PUBLIC_KEY_PATH
from .config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from .models import Kubernetes, RedisConnector, Database
from jwt import decode
import json

db: Database
key: str

@asynccontextmanager
async def init(app: FastAPI):
    global db
    global key
    db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
    try:
        with(open(PUBLIC_KEY_PATH, "r")) as f:
            key = f.read()
    except:
        raise HTTPException(status_code=500, detail="Public key not found")
    yield

app = FastAPI(lifespan=init,
              root_path="/api/admin")

class Challenge(BaseModel):
    name: str
    description: str
    image: str
    ports: list[int]
    category: str

def create_service_manifest(name, ports):
    return {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": name
        },
        "spec": {
            "selector": {
                "app": name
            },
            "ports": [
                {
                    "protocol": "TCP",
                    "port": port,
                    "targetPort": port
                } for port in ports
            ]
        }
    }

def create_pod_manifest(name, image, ports):
    return {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": name,
            "labels": {
                "app": name
            }
        },
        "spec": {
            "containers": [
                {
                    "name": name,
                    "image": image,
                    "ports": [
                        {
                            "containerPort": port
                        } for port in ports
                    ]
                }
            ]
        }
    }



@app.post("/challenge")
def create_challenge(challenge: Challenge, x_token: str = Header()):
    token = None
    try:
        print(x_token)
        print(key)
        token = decode(x_token, key, algorithms=["RS256"])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    print(token)
    if not token.get("admin"):
        raise HTTPException(status_code=401, detail="Invalid token")
    service_manifest = json.dumps(create_service_manifest(challenge.name, challenge.ports))
    pod_manifest = json.dumps(create_pod_manifest(challenge.name, challenge.image, challenge.ports))
    chall = db.add_challenge(challenge.name, challenge.description, challenge.category)
    print("id: ", chall)
    img = db.add_image(chall, pod_manifest)
    db.add_service(img, service_manifest)
    return {"status": "ok"}

class Flag(BaseModel):
    flag: str
    challenge_id: int
    points: int

@app.post("/flag")
def create_flag(flag: Flag, x_token: str = Header()):
    token = None
    try:
        token = decode(x_token, key, algorithms=["RS256"])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    if not token.get("admin"):
        raise HTTPException(status_code=401, detail="Invalid token")
    db.add_flag(flag.flag, flag.challenge_id, flag.points)
    return {"status": "ok"}

class User(BaseModel):
    password: str|None
    is_admin: bool|None

@app.put("/user/{user_id}")
def update_user(user_id: int, user: User, x_token: str = Header()):
    token = None
    try:
        token = decode(x_token, key, algorithms=["RS256"])
    except:
        print("ERROR")
        raise HTTPException(status_code=401, detail="Invalid token")
    print(token)
    if not token.get("admin"):
        raise HTTPException(status_code=401, detail="Invalid token")
    db.update_user(user_id, user.password, user.is_admin)
    return {"status": "ok"}



@app.get("/health")
def health():
    return {"status": "ok"}
