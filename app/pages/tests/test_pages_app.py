import json

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from app.pages.models import Page
from app.setup.models import SiteSettings


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


class FooterBlockDefaultsTests(TestCase):
    def setUp(self):
        self.settings = SiteSettings.get_solo()
        self.settings.org_name = "Contrast"
        self.settings.address_street = "Josef-Belli-Weg"
        self.settings.address_number = "4"
        self.settings.address_postal_code = "78467"
        self.settings.address_city = "Konstanz"
        self.settings.address_country = "Germany"
        self.settings.social_instagram = "https://instagram.com/contrast"
        self.settings.social_facebook = "https://facebook.com/contrast"
        self.settings.save()

    def test_footer_block_autopopulates_from_site_settings(self):
        page = Page.objects.create(
            title="Home",
            slug="home-footer",
            blocks=[
                {"id": "hero", "type": "rich_text", "props": {"html": "<p>Body</p>"}},
                {"id": "footer-1", "type": "footer", "props": {}},
            ],
            status=Page.Status.PUBLISHED,
            is_visible=True,
        )

        html = page.render_content()

        self.assertIn("Contrast", html)
        self.assertIn("Josef-Belli-Weg 4", html)
        self.assertIn("78467 Konstanz", html)
        self.assertIn('aria-label="Instagram"', html)

    def test_render_content_segments_places_footer_separately(self):
        page = Page.objects.create(
            title="Home",
            slug="home-footer-split",
            blocks=[
                {"id": "hero", "type": "rich_text", "props": {"html": "<p>Body</p>"}},
                {"id": "footer-1", "type": "footer", "props": {}},
            ],
            status=Page.Status.PUBLISHED,
            is_visible=True,
        )

        main_html, footer_html, nav_html = page.render_content_segments()

        self.assertIn("Body", main_html)
        self.assertNotIn("page-block--footer", main_html)
        self.assertIn("page-block--footer", footer_html)
        self.assertIn("page-block--navigation", nav_html)

    def test_set_blocks_for_language_override(self):
        page = Page.objects.create(
            title="Home",
            slug="home",
            blocks=[{"id": "hero", "type": "rich_text", "props": {"html": "<p>Base</p>"}}],
            status=Page.Status.PUBLISHED,
            is_visible=True,
        )

        page.set_blocks_for_language("de", [{"id": "hero", "type": "rich_text", "props": {"html": "<p>DE</p>"}}], override=True)
        self.assertIn("de", page.layout_overrides)
        self.assertEqual(page.get_blocks_for_language("de")[0]["props"]["html"], "<p>DE</p>")

        page.set_blocks_for_language("de", [{"id": "hero", "type": "rich_text", "props": {"html": "<p>Shared</p>"}}], override=False)
        self.assertNotIn("de", page.layout_overrides)
        self.assertEqual(page.get_blocks_for_language("de")[0]["props"]["html"], "<p>Shared</p>")

    def test_shared_layout_updates_from_non_default_language(self):
        page = Page.objects.create(
            title="Home",
            slug="home-shared",
            blocks=[],
            status=Page.Status.PUBLISHED,
            is_visible=True,
        )

        page.set_blocks_for_language(
            "de",
            [{"id": "hero", "type": "rich_text", "props": {"html": "<p>DE layout</p>"}}],
            override=False,
        )

        self.assertNotIn("de", page.layout_overrides)
        self.assertEqual(page.get_blocks_for_language("en")[0]["props"]["html"], "<p>DE layout</p>")
        self.assertEqual(page.get_blocks_for_language("fr")[0]["props"]["html"], "<p>DE layout</p>")

    def test_language_translation_used_even_without_override_flag(self):
        page = Page.objects.create(
            title="Home",
            slug="home-legacy",
            blocks=[],
            status=Page.Status.PUBLISHED,
            is_visible=True,
        )
        page.layout_overrides = []
        page.__dict__[page._meta.get_field("blocks").attname] = []
        setattr(
            page,
            "blocks_es",
            [{"id": "hero", "type": "rich_text", "props": {"html": "<p>Legacy ES</p>"}}],
        )

        self.assertEqual(page.get_blocks_for_language("es")[0]["props"]["html"], "<p>Legacy ES</p>")


class LoginDevButtonTests(TestCase):
    @override_settings(ENV="development", DEBUG=False)
    def test_login_page_shows_dev_button_when_dev_env(self):
        settings_obj = SiteSettings.get_solo()
        settings_obj.dev_login_enabled = True
        settings_obj.save()

        response = self.client.get(reverse("login"))

        self.assertContains(response, "Force Login (Dev)")
