from app.domain.tags.entities import Tag


class TestTagEntity:
    def test_create_tag(self):
        tag = Tag(name="Technology", slug="technology")
        assert tag.name == "Technology"
        assert tag.slug == "technology"
        assert tag.is_active is True
        assert tag.id is None

    def test_tag_with_all_fields(self):
        tag = Tag(name="Tech", slug="tech", description="Tech posts", is_active=False, id=1)
        assert tag.id == 1
        assert tag.description == "Tech posts"
        assert tag.is_active is False
