from pathlib import Path
from datetime import datetime
import time


LOG_DIR = Path("logs")

LOG_FILE = LOG_DIR / "app.log"


def log_request(
    query,
    route,
    model,
    session_id,
    start_time
):

    latency = round(

        time.time() - start_time,

        3

    )

    timestamp = datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )

    LOG_DIR.mkdir(

        exist_ok=True

    )

    log_text = f"""
{timestamp}

Session: {session_id}

Query: {query}

Route: {route}

Model: {model}

Latency: {latency} sec

----------------------------------------
"""

    # Console

    print(

        "\n===== REQUEST LOG ====="

    )

    print(

        f"Session: {session_id}"

    )

    print(

        f"Query: {query}"

    )

    print(

        f"Route: {route}"

    )

    print(

        f"Model: {model}"

    )

    print(

        f"Latency: {latency} sec"

    )

    print(

        "======================"

    )

    # File

    with open(

        LOG_FILE,

        "a",

        encoding="utf-8"

    ) as file:

        file.write(

            log_text

        )
