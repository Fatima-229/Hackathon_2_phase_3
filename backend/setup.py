from setuptools import setup, find_packages

setup(
    name="todo-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.128.5",
        "sqlmodel==0.0.32",
        "uvicorn==0.40.0",
        "psycopg2-binary==2.9.11",
        "python-jose[cryptography]==3.5.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.22",
        "pydantic-settings==2.12.0",
    ],
    author="Todo App Developer",
    author_email="dev@example.com",
    description="A full-stack todo application backend",
    python_requires=">=3.7",
)