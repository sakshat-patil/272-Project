import uvicorn
from dotenv import load_dotenv

# Load environment variables before starting the server
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True  # Enable auto-reload during development
    )