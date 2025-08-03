import boto3
import json
import uuid
import datetime
import random

s3 = boto3.client('s3')
bucket_name = "ci-cd-portfolio-dev-data"

def generate_log_event():
    return {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "user_id": f"user_{random.randint(100, 999)}",
        "event_type": random.choice(["login", "purchase", "logout"]),
        "ip": f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"
    }

def write_logs_to_s3(n=100):
    for _ in range(n):
        log = generate_log_event()
        key = f"raw/dt={datetime.date.today()}/log_{uuid.uuid4()}.json"
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(log))
        print(f"Uploaded: {key}")

if __name__ == "__main__":
    write_logs_to_s3(n=10)