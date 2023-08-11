<img title="ITishAPI" alt="Header image" src="./header.png">

_API (FastAPI) for my blog site [ITish](https://itish.live)_

## Purpose

My blog site [ITish](https://itish.live) ([GitHub](https://github.com/Gubchik123/ITish)) was written using templates, but in our time there are not a lot of projects that use templates. That's why here is API of the "ITish"

## Project modules

<a href='https://pypi.org/project/fastapi'><img alt='fastapi' src='https://img.shields.io/pypi/v/fastapi?label=fastapi&color=blue'></a> <a href='https://pypi.org/project/python-dotenv'><img alt='python-dotenv' src='https://img.shields.io/pypi/v/python-dotenv?label=python-dotenv&color=blue'></a> <a href='https://pypi.org/project/python-jose'><img alt='python-jose' src='https://img.shields.io/pypi/v/python-jose?label=python-jose&color=blue'></a> <a href='https://pypi.org/project/SQLAlchemy'><img alt='SQLAlchemy' src='https://img.shields.io/pypi/v/SQLAlchemy?label=SQLAlchemy&color=blue'></a> 

> Look at the requirements.txt

## Environment Variables

To run this project, you will need to add the following environment variables:

`DATABASE_URL`
`JWT_SECRET_KEY` `JWT_REFRESH_SECRET_KEY`

> Look at the file_env_example.txt

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:
    ```
    git clone https://github.com/Gubchik123/ITishAPI.git
    ```

2. Go to the project directory:

    ```
    cd ITishAPI
    ```

3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

5. Run the uvicorn development server:
    ```
    uvicorn main:app
    ```

    > **Note:** Don't forget about environment variables