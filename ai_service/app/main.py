from fastapi import FastAPI
from app.integrations.google.credentials import (
    GoogleCredentialsProvider)


app = FastAPI(title="AI Service")


@app.get("/")
async def read_root() -> dict[str, str]:

    provider = GoogleCredentialsProvider()

    print("Credentials file:", provider.credentials_file)
    print("Service account:", provider.service_account_email)
    print("Scopes:", provider.credentials.scopes)
    return {"message": "AI service is running"}
