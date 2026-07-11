from app.integrations.google.credentials import (
    GoogleCredentialsProvider,
)


provider = GoogleCredentialsProvider()

print("Credentials file:", provider.credentials_file)
print("Service account:", provider.service_account_email)
print("Scopes:", provider.credentials.scopes)