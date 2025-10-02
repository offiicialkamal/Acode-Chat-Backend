import uvicorn
from main import asgi_app  # your Flask app object

if __name__ == "__main__":
    # Option 1: pass the app object directly
    # uvicorn.run(asgi_app, host="0.0.0.0", port=5000)
    uvicorn.run("main:asgi_app", host="0.0.0.0", port=5000, lifespan="off")
    # Option 2: pass as string "module:app"
    # uvicorn.run("app:app", host="0.0.0.0", port=8000)
    
