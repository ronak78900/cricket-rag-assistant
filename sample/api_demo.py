import os

import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://jsonplaceholder.typicode.com/todos/1"


def fetch_title() -> str:
    key = os.getenv("DEMO_API_KEY")
    response = requests.get(
        URL,
        headers={"Authorization": f"Bearer {key}"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["title"]


if __name__ == "__main__":
    print(fetch_title())