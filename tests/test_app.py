def auth(client, username):
    client.post("/auth/register", json={"username": username, "password": "secret123"})
    response = client.post("/auth/login", data={"username": username, "password": "secret123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_register_and_login(client):
    headers = auth(client, "alice")
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "alice"


def test_wrong_password(client):
    client.post("/auth/register", json={"username": "bob", "password": "secret123"})
    response = client.post("/auth/login", data={"username": "bob", "password": "wrong"})
    assert response.status_code == 401


def test_posts_comments_and_rbac(client):
    admin = auth(client, "admin")
    user = auth(client, "user")
    created = client.post("/posts", json={"title": "Hello", "content": "World"}, headers=user)
    assert created.status_code == 201
    post_id = created.json()["id"]
    assert len(client.get("/posts").json()) == 1
    comment = client.post(f"/posts/{post_id}/comments", json={"text": "Nice"}, headers=user)
    assert comment.status_code == 201
    assert len(client.get(f"/posts/{post_id}/comments").json()) == 1
    assert client.delete(f"/posts/{post_id}", headers=user).status_code == 403
    assert client.delete(f"/posts/{post_id}", headers=admin).status_code == 204
    assert client.get(f"/posts/{post_id}").status_code == 404
