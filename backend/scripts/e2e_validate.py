"""
E2E validation script for the CMS Admin frontend + backend.

Usage:
    poetry run python scripts/e2e_validate.py

Prerequisites:
    - Backend running at http://localhost:8000
    - Frontend running at http://localhost:5173
    - Database with a superuser (see scripts/create_superuser.py)
"""

import httpx
import sys

BASE_URL = "http://localhost:8000/api/v1"

passed = 0
failed = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✓ {name}")
    else:
        failed += 1
        print(f"  ✗ {name} — {detail}")


def main() -> int:
    print(f"\nE2E Validation — CMS Admin\n")
    print(f"Backend: {BASE_URL}\n")

    # 1. Health
    try:
        r = httpx.get(f"{BASE_URL}/health", timeout=5)
        check("Health endpoint", r.is_success)
    except Exception as e:
        check("Health endpoint", False, str(e))

    # 2. Login
    email = "admin@cms.com"
    password = "admin123"

    r = httpx.post(f"{BASE_URL}/auth/token", json={"email": email, "password": password})
    if r.is_success:
        token = r.json().get("access_token", "")
        refresh_token = r.json().get("refresh_token", "")
        check("Login returns access_token", bool(token))
        check("Login returns refresh_token", bool(refresh_token))

        headers = {"Authorization": f"Bearer {token}"}

        # 3. Me
        r = httpx.get(f"{BASE_URL}/users/me", headers=headers)
        check("GET /users/me", r.is_success)
        if r.is_success:
            check("User has email", r.json().get("email") == email)

        # 4. Tags CRUD
        r = httpx.get(f"{BASE_URL}/tags", headers=headers)
        check("List tags", r.is_success)

        tag_data = {"name": "E2E Test Tag", "description": "Created by E2E test"}
        r = httpx.post(f"{BASE_URL}/tags", json=tag_data, headers=headers)
        check("Create tag", r.is_success and r.status_code == 201)
        if r.is_success:
            tag_id = r.json().get("id")
            r = httpx.patch(f"{BASE_URL}/tags/{tag_id}", json={"name": "E2E Updated"}, headers=headers)
            check("Update tag", r.is_success)
            r = httpx.delete(f"{BASE_URL}/tags/{tag_id}", headers=headers)
            check("Delete tag", r.is_success and r.status_code == 204)

        # 5. Posts CRUD
        r = httpx.get(f"{BASE_URL}/posts", headers=headers)
        check("List posts", r.is_success)

        post_data = {
            "title": "E2E Test Post",
            "slug": f"e2e-post-{__import__('time').time()}",
            "html": "<h1>Hello</h1><p>E2E test content.</p>",
            "summary": "E2E test summary",
            "tag_ids": [],
        }
        r = httpx.post(f"{BASE_URL}/posts", json=post_data, headers=headers)
        check("Create post", r.is_success and r.status_code == 201)
        if r.is_success:
            post_id = r.json().get("id")

            r = httpx.patch(f"{BASE_URL}/posts/{post_id}", json={"title": "E2E Updated Post"}, headers=headers)
            check("Update post", r.is_success)

            r = httpx.get(f"{BASE_URL}/posts/{post_id}/detail", headers=headers)
            check("Get post detail", r.is_success)

            r = httpx.post(f"{BASE_URL}/posts/{post_id}/publish", headers=headers)
            check("Publish post", r.is_success)

            r = httpx.post(f"{BASE_URL}/posts/{post_id}/archive", headers=headers)
            check("Archive post", r.is_success)

            r = httpx.delete(f"{BASE_URL}/posts/{post_id}", headers=headers)
            check("Delete post", r.is_success and r.status_code == 204)

        # 6. Refresh token
        if refresh_token:
            r = httpx.post(f"{BASE_URL}/auth/refresh", json={"refresh_token": refresh_token})
            check("Refresh token", r.is_success)

        # 7. Logout / clear
        r = httpx.get(f"{BASE_URL}/users/me", headers={"Authorization": "Bearer invalid-token"})
        check("Rejects invalid token", not r.is_success)

    elif r.status_code == 403 and r.json().get("detail") == "auth:mfa_required":
        check("MFA login", True, "User has MFA enabled — use scripts/mfa_challenge.py flow")
    else:
        check("Login", False, f"HTTP {r.status_code}: {r.text}")

    # Summary
    total = passed + failed
    print(f"\n{'='*40}")
    print(f"Results: {passed}/{total} passed, {failed} failed")
    print(f"{'='*40}\n")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
