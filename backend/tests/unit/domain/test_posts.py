from uuid import uuid4

from app.domain.posts.entities import Post


class TestPostEntity:
    def test_create_post(self):
        author_id = uuid4()
        post = Post(title="My Post", slug="my-post", author_id=author_id)
        assert post.title == "My Post"
        assert post.slug == "my-post"
        assert post.author_id == author_id
        assert post.status == "draft"

    def test_post_with_tag_ids(self):
        author_id = uuid4()
        post = Post(title="Post", slug="post", author_id=author_id, tag_ids=[1, 2, 3])
        assert post.tag_ids == [1, 2, 3]
