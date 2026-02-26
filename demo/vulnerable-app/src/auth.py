"""
Demo: Vulnerable Authentication Module
⚠️  INTENTIONALLY VULNERABLE — For SecureFlow demo purposes only
⚠️  DO NOT use in production

This file contains intentional security vulnerabilities that SecureFlow
will detect and fix in the demo:
1. SQL Injection (line ~30)
2. Hardcoded secret (line ~15)
3. Insecure password comparison (line ~45)
"""

import sqlite3
import hashlib
import os

# ⚠️ VULNERABILITY 1: Hardcoded secret (CWE-798)
# SecureFlow fix: Move to os.environ.get('SECRET_KEY')
SECRET_KEY = "super-secret-key-abc123-do-not-share"
JWT_SECRET = "jwt-secret-hardcoded-12345"

# Database connection
DB_PATH = "users.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def login(username: str, password: str) -> dict:
    """
    Authenticate a user.
    
    ⚠️ VULNERABILITY 2: SQL Injection (CWE-89)
    SecureFlow fix: Use parameterized queries
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string interpolation — attacker can inject SQL
    # e.g., username = "admin' OR '1'='1" bypasses authentication
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)  # SQL INJECTION HERE
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"success": True, "user_id": user[0], "username": user[1]}
    return {"success": False}


def get_user_data(user_id: str) -> dict:
    """
    Get user profile data.
    
    ⚠️ VULNERABILITY 3: Another SQL Injection (CWE-89)
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # VULNERABLE: user_id from URL parameter injected directly
    cursor.execute("SELECT * FROM users WHERE id = " + user_id)
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {"id": row[0], "username": row[1], "email": row[2]}
    return {}


def reset_password(email: str, new_password: str) -> bool:
    """
    Reset user password.
    
    ⚠️ VULNERABILITY 4: Weak password hashing (CWE-916)
    SecureFlow fix: Use bcrypt or argon2
    """
    # VULNERABLE: MD5 is cryptographically broken for passwords
    hashed = hashlib.md5(new_password.encode()).hexdigest()
    
    conn = get_db()
    cursor = conn.cursor()
    # VULNERABLE: SQL injection in email parameter
    cursor.execute(f"UPDATE users SET password='{hashed}' WHERE email='{email}'")
    conn.commit()
    conn.close()
    return True


def verify_admin_token(token: str) -> bool:
    """
    Verify admin access token.
    
    ⚠️ VULNERABILITY 5: Hardcoded admin token (CWE-798)
    """
    # VULNERABLE: Hardcoded token — anyone with source access is admin
    ADMIN_TOKEN = "admin-token-secret-2024"
    return token == ADMIN_TOKEN
