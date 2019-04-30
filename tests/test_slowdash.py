import pytest

from slowdash import slowdash
from slowdash.server.models import Post


@pytest.fixture
def client():
    slowdash.app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://yura@/test_slowdash"
    slowdash.app.config["TESTING"] = True
    client = slowdash.app.test_client()

    with slowdash.app.app_context():
        slowdash.db.drop_all()
        slowdash.db.create_all()
        post = Post(title="test title", body="test body")
        slowdash.db.session.add(post)
        slowdash.db.session.commit()

    yield client


def test_get_posts(client):
    """Get list of posts."""
    res = client.get("/api/blog/posts")

    assert res.status_code == 200
    posts = res.get_json()
    assert posts[0]["title"] == "test title"
    assert posts[0]["body"] == "test body"


def test_create_post(client):
    """Create a new blog post."""
    res = client.post(
        "/api/blog/posts",
        data={"title": "second test title", "body": "testing second body"},
    )

    # Check if response is correct.
    assert res.status_code == 201
    post = res.get_json()
    assert post["title"] == "second test title"
    assert post["body"] == "testing second body"

    # Check if list of posts is properly updated.
    posts = client.get("/api/blog/posts").get_json()
    assert posts[0]["title"] == "test title"
    assert posts[0]["body"] == "test body"
    assert posts[1]["title"] == "second test title"
    assert posts[1]["body"] == "testing second body"
