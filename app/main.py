import os
from fastapi import FastAPI

app = FastAPI(title="Python FastAPI DevSecOps PoC", version="1.0.0")

def load_vault_secrets():
    """Simulates reading dynamic secrets injected by HashiCorp Vault Agent"""
    secret_path = "/vault/secrets/db-creds"
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            return f.read().strip()
    return "No Vault Secrets Injected - Using Local Fallback"

@app.get("/")
def read_root():
    return {
        "status": "Healthy",
        "framework": "FastAPI",
        "mesh": "Istio Ready"
    }

@app.get("/secure-data")
def read_secrets():
    secret_content = load_vault_secrets()
    return {
        "vault_status": "Connected" if "No Vault" not in secret_content else "Standalone",
        "data": secret_content
    }

@app.get("/healthz")
def health_check():
    # Dedicated endpoint for Kubernetes liveness/readiness probes
    return {"status": "UP"}
