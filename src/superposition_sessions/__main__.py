"""Run the session room: python -m superposition_sessions"""

import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "7841"))
    uvicorn.run(
        "superposition_sessions.web.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
