#!/usr/bin/env python3
"""
Script to run the Todo API backend server.

This script starts the FastAPI server with the proper configuration.
By default, it runs on port 8000 as specified in the config, but can be overridden.
"""

import uvicorn
from main import app
from config import settings


def main():
    """Main function to run the server."""
    print(f"Starting Todo API server on {settings.api_host}:{settings.api_port}")
    print(f"API documentation available at: http://{settings.api_host}:{settings.api_port}/docs")
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=False,  # Set to True for development to enable auto-reload
    )


if __name__ == "__main__":
    main()