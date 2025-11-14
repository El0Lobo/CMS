import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from app.pages.models import Page


class PageRenderContentTests(TestCase):
    def setUp(self):
        self.blocks = [
            {
                "id": "block-1",
                "type": "rich_text",
                "props": {"html": "<p>Builder content</p>"},
            }
        ]

    def test_render_content_prefers_blocks_when_enabled(self):
        page = Page.objects.create(
            title="Story",
            slug="story",
            body="<p>Raw body</p>",
            blocks=self.blocks,
            status=Page.Status.PUBLISHED,
            is_visible=True,
            render_body_only=False,
        )

        rendered = page.render_content()

        self.assertIn("Builder content", rendered)
        self.assertIn("page-block--richtext", rendered)
        self.assertNotIn("Raw body", rendered)

    def test_render_content_respects_render_body_only_toggle(self):
        page = Page.objects.create(
            title="Story",
            slug="story-raw",
            body="<p>Raw body</p>",
            blocks=self.blocks,
            status=Page.Status.PUBLISHED,
            is_visible=True,
            render_body_only=True,
        )

        rendered = page.render_content()

        self.assertIn("Raw body", rendered)
        self.assertNotIn("page-block--richtext", rendered)


class PreviewHtmlApiTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user("author", "author@example.com", "password123")
        self.client.force_login(self.user)

        # Navigation source so build_nav_payload can resolve the slug.
        self.nav_page = Page.objects.create(
            title="Home",
            slug="home",
            status=Page.Status.PUBLISHED,
            is_visible=True,
        )

        self.url = reverse("pages_api_preview_html")
        self.blocks = [
            {
                "id": "block-1",
                "type": "rich_text",
                "props": {"html": "<p>Builder preview</p>"},
            }
        ]

    def post_preview(self, **overrides):
        payload = {
            "title": "Preview page",
            "slug": "preview-page",
            "blocks": self.blocks,
            "body": "<p>Raw preview</p>",
            "render_body_only": False,
            "show_navigation_bar": True,
            "custom_nav_items": ["home"],
        }
        payload.update(overrides)
        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        return response.json()

    def test_preview_html_returns_block_markup_by_default(self):
        data = self.post_preview()

        self.assertIn("page-block--richtext", data["content_html"])
        self.assertIn("Builder preview", data["content_html"])
        # Navigation payload should render the Home link (pretty URL "/").
        self.assertIn('href="/"', data["html"])

    def test_preview_html_respects_render_body_only_flag(self):
        data = self.post_preview(render_body_only=True)

        self.assertIn("Raw preview", data["content_html"])
        self.assertNotIn("page-block--richtext", data["content_html"])
