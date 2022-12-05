import uuid
import requests
from cryptography.fernet import Fernet

sync = requests.get("http://localhost:8000/student/synchronize")                    # First synchronized query

json = sync.json()
secret_uuid = json["data"][0]
common_key = Fernet("ENEou4JUwaA0tgBfxUpPgvtOmJW5YQztdwKA4if8vUQ=") 
uuid_t = common_key.decrypt(secret_uuid)                                            # Decrypt secret uuid for unique link
answer = requests.get(f"http://localhost:8000/student/+{uuid.UUID(uuid_t.hex())}" ) # Needed query

print(answer.json())