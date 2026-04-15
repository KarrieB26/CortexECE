from fastapi import FastAPI

app = FastAPI(title="CortextECE API")

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}
