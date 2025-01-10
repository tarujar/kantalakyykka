from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.router import api_router  # Ensure this import is correct

app = FastAPI()

# Include the API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")

# Ensure the app instance is correctly defined
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
