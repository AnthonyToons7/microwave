import os
import re
import subprocess
import json

CURL_DIR = os.path.join(os.path.dirname(__file__), "..", "curls")

def extract_token(stdout: str) -> str | None:
    try:
        data = json.loads(stdout)
        return data.get("access_token")
    except Exception:
        return None

def update_bearer_token(curl_name: str, new_token: str):
    path = os.path.join(CURL_DIR, f"{curl_name}.txt")

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    content = re.sub(
        r'Authorization:\s*Bearer\s+[^\s"]+',
        f'Authorization: Bearer {new_token}',
        content
    )

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

def get_curl_dir():
    return os.path.abspath(CURL_DIR)

def get_curl_files():
    if not os.path.exists(CURL_DIR):
        os.makedirs(CURL_DIR)

    return [
        os.path.splitext(file)[0]
        for file in os.listdir(CURL_DIR)
        if file.lower().endswith(".txt")
    ]

def parse_curl_file(name):
    path = os.path.join(CURL_DIR, f"{name}.txt")

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    def extract(section):
        match = re.search(
            rf"\[{section}\](.*?)(?:\n\[|\Z)",
            content,
            re.S | re.I
        )
        return match.group(1).strip() if match else None

    meta = extract("META") or ""
    to_execute = extract("TO_EXECUTE")
    on_unauth = extract("ON_UNAUTHENTICATED")

    method_match = re.search(r"METHOD\s*=\s*(\w+)", meta, re.I)
    method = method_match.group(1).upper() if method_match else "POST"

    return {
        "name": name,
        "method": method,
        "main": to_execute,
        "unauth": on_unauth
    }

def execute_curl_bundle(bundle):
    def run(cmd):
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)

    init_command = force_method(bundle["main"], bundle["method"])
    init_command += ' -w "\\nHTTP_CODE:%{http_code}"'
    result = run(init_command)

    if "HTTP_CODE:401" in result.stdout and bundle.get("unauth"):
        login = run(bundle["unauth"])
        token = extract_token(login.stdout)

        if token:
            update_bearer_token(bundle["name"], token)
            refreshed_bundle = parse_curl_file(bundle["name"])
            retry_cmd = force_method(
                refreshed_bundle["main"],
                refreshed_bundle["method"]
            )
            retry_cmd += ' -w "\\nHTTP_CODE:%{http_code}"'

            return run(retry_cmd)

    print(result)
    return result

def force_method(curl_cmd, method):
    curl_cmd = re.sub(r'-X\s+\w+', '', curl_cmd)
    return curl_cmd.replace("curl ", f"curl -X {method} ", 1)