from fastapi import FastAPI
from routers.items import router  # Import the router object

app = FastAPI(title="App", description="Service to manage Items")

# Include the router object in the application
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # Adjust host, port, and reload as needed
