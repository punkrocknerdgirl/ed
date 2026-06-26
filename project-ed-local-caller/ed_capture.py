import json
import os
import sys
from urllib import request, error


def load_dotenv(path=".env"):
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def post_capture(text, source="local", category="project_ed"):
    load_dotenv()

    broker_url = os.environ.get("ED_BROKER_URL")
    secret = os.environ.get("ED_BROKER_SECRET")

    if not broker_url:
        raise RuntimeError("Missing ED_BROKER_URL. Add it to .env or environment variables.")

    if not secret:
        raise RuntimeError("Missing ED_BROKER_SECRET. Add it locally. Do not paste it into chat.")

    payload = {
        "secret": secret,
        "action": "captureNote",
        "text": text,
        "source": source,
        "category": category,
    }

    body = json.dumps(payload).encode("utf-8")

    req = request.Request(
        broker_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8")

    except error.HTTPError as e:
        details = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {details}") from e

    except error.URLError as e:
        raise RuntimeError(f"Could not reach broker: {e.reason}") from e


def main():
    if len(sys.argv) < 2:
        print('Usage: python ed_capture.py "note text here" [category]')
        sys.exit(1)

    text = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) >= 3 else "project_ed"

    result = post_capture(text=text, category=category)
    print(result)


if __name__ == "__main__":
    main()
