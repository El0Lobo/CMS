"""
Management command to seed the database with realistic test data.
Similar to Rails seeds - populates the database with sample data for local development.
"""

from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import OperationalError, ProgrammingError
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with realistic test data (development/test environments only)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing seed data before creating new data",
        )

    def check_migrations(self):
        """Check if migrations have been run."""
        try:
            # Try to access the auth_user table as a sanity check
            User.objects.exists()
            return True
        except (OperationalError, ProgrammingError):
            return False

    def handle(self, *args, **options):
        # Only allow seeding in development/test environments
        if settings.ENV not in ("development", "test"):
            self.stderr.write(
                self.style.ERROR(
                    f"Refusing to run in {settings.ENV} environment. "
                    "Set DJANGO_ENV=development to enable seeding."
                )
            )
            return

        # Check if migrations have been run
        if not self.check_migrations():
            self.stderr.write(self.style.ERROR("\n✗ Database tables don't exist!"))
            self.stderr.write(self.style.ERROR("Please run migrations first:"))
            self.stderr.write(self.style.WARNING("  python manage.py migrate"))
            self.stderr.write(self.style.WARNING("Or run the full setup:"))
            self.stderr.write(self.style.WARNING("  ./bin/setup"))
            return

        self.stdout.write(self.style.WARNING("Starting database seeding..."))

        try:
            with transaction.atomic():
                if options["clear"]:
                    self.clear_data()

                self.seed_users()
                self.seed_pages()
                self.seed_events()
                self.seed_menu_items()
                self.seed_merch()
                self.seed_bands()
                self.seed_site_settings()

            self.stdout.write(self.style.SUCCESS("\n✓ Database seeded successfully!"))
            self.stdout.write("\nYou can now log in with:")
            self.stdout.write("  - Username: admin / Password: admin123 (superuser)")
            self.stdout.write("  - Username: staff / Password: staff123 (staff)")
            self.stdout.write("  - Username: user / Password: user123 (regular user)")

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"\n✗ Seeding failed: {e}"))
            raise

    def clear_data(self):
        """Clear existing seed data (optional)."""
        self.stdout.write("Clearing existing seed data...")

        # Import models dynamically to avoid import errors if apps don't exist
        try:
            from app.events.models import Event, EventCategory

            Event.objects.all().delete()
            EventCategory.objects.all().delete()
        except (ImportError, OperationalError, ProgrammingError):
            pass

        try:
            from app.menu.models import Item

            Item.objects.all().delete()
        except (ImportError, OperationalError, ProgrammingError):
            pass

        try:
            from app.merch.models import Product

            Product.objects.all().delete()
        except (ImportError, OperationalError, ProgrammingError):
            pass

        try:
            from app.bands.models import Band

            Band.objects.all().delete()
        except (ImportError, OperationalError, ProgrammingError):
            pass

        # Note: We don't clear Pages as they may be important
        # Pages will be created with unique slugs using get_or_create

        self.stdout.write(self.style.SUCCESS("  ✓ Cleared existing data"))

    def seed_users(self):
        """Create test users with different permission levels."""
        self.stdout.write("Seeding users...")

        # Admin user (should already exist from create_dev_admin)
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
                "first_name": "Admin",
                "last_name": "User",
            },
        )
        if created:
            admin.set_password("admin123")
            admin.save()

        # Staff user
        staff, created = User.objects.get_or_create(
            username="staff",
            defaults={
                "email": "staff@example.com",
                "is_staff": True,
                "is_superuser": False,
                "first_name": "Staff",
                "last_name": "Member",
            },
        )
        if created:
            staff.set_password("staff123")
            staff.save()

        # Regular user
        user, created = User.objects.get_or_create(
            username="user",
            defaults={
                "email": "user@example.com",
                "is_staff": False,
                "is_superuser": False,
                "first_name": "Regular",
                "last_name": "User",
            },
        )
        if created:
            user.set_password("user123")
            user.save()

        self.stdout.write(self.style.SUCCESS("  ✓ Created test users"))

    def seed_pages(self):
        """Create sample CMS pages with smart, realistic content and block structures."""
        self.stdout.write("Seeding pages...")

        try:
            from django.utils import timezone

            from app.pages.models import Page

            # Get admin user for created_by field
            try:
                admin_user = User.objects.get(username="admin")
            except User.DoesNotExist:
                admin_user = None

            pages_data = [
                {
                    "title_en": "Home",
                    "title_es": "Inicio",
                    "title_de": "Startseite",
                    "title_fr": "Accueil",
                    "slug_en": "home",
                    "slug_es": "inicio",
                    "slug_de": "startseite",
                    "slug_fr": "accueil",
                    "summary_en": "Welcome to our community venue - your local spot for great music, drinks, and events",
                    "summary_es": "Bienvenido a nuestro local comunitario - tu lugar local para buena música, bebidas y eventos",
                    "summary_de": "Willkommen in unserem Veranstaltungsort - dein lokaler Ort für gute Musik, Getränke und Events",
                    "summary_fr": "Bienvenue dans notre lieu communautaire - votre endroit local pour de la bonne musique, des boissons et des événements",
                    "body_en": "",
                    "body_es": "",
                    "body_de": "",
                    "body_fr": "",
                    "status": "published",
                    "is_visible": True,
                    "navigation_order": 0,
                    "show_navigation_bar": True,
                    "custom_nav_items": [],
                    "render_body_only": False,
                    "blocks_en": [
                        {
                            "id": "323a4398-5412-4a5d-8c53-c57060db0d77",
                            "type": "hero",
                            "props": {
                                "kicker": "Welcome to",
                                "title": "Our Community Space",
                                "subtitle": "A local venue bringing people together through music, art, and great drinks. Experience the vibrant atmosphere of our neighborhood gathering spot.",
                                "background_image": "",
                                "overlay": 0.45,
                                "alignment": "center",
                                "actions": [],
                            },
                        },
                        {
                            "id": "50249da0-a80a-4242-b9ff-03d08f54dcaa",
                            "type": "contact",
                            "props": {"show_social": True},
                        },
                        {
                            "id": "efcad5d3-7731-4bf8-9596-23fafd4f21c6",
                            "type": "menu",
                            "props": {
                                "title": "Menu Highlights",
                                "subtitle": "Check out our selection of drinks and snacks",
                                "category_slugs": [],
                            },
                        },
                        {
                            "id": "214f2243-6f37-4f4a-bba2-ef132a1072c6",
                            "type": "footer",
                            "props": {
                                "brand_name": "",
                                "brand_tagline": "",
                                "brand_logo": "",
                                "address_html": "",
                                "links": [],
                                "legal": [],
                                "social_links": [],
                                "show_social": True,
                            },
                        },
                    ],
                    "blocks_es": [
                        {
                            "id": "323a4398-5412-4a5d-8c53-c57060db0d77",
                            "type": "hero",
                            "props": {
                                "kicker": "Bienvenido a",
                                "title": "Nuestro Espacio Comunitario",
                                "subtitle": "Un lugar local que reúne a las personas a través de la música, el arte y excelentes bebidas. Experimenta la atmósfera vibrante de nuestro punto de encuentro del vecindario.",
                                "background_image": "",
                                "overlay": 0.45,
                                "alignment": "center",
                                "actions": [],
                            },
                        },
                        {
                            "id": "50249da0-a80a-4242-b9ff-03d08f54dcaa",
                            "type": "contact",
                            "props": {"show_social": True},
                        },
                        {
                            "id": "efcad5d3-7731-4bf8-9596-23fafd4f21c6",
                            "type": "menu",
                            "props": {
                                "title": "Destacados del Menú",
                                "subtitle": "Descubre nuestra selección de bebidas y aperitivos",
                                "category_slugs": [],
                            },
                        },
                        {
                            "id": "214f2243-6f37-4f4a-bba2-ef132a1072c6",
                            "type": "footer",
                            "props": {
                                "brand_name": "",
                                "brand_tagline": "",
                                "brand_logo": "",
                                "address_html": "",
                                "links": [],
                                "legal": [],
                                "social_links": [],
                                "show_social": True,
                            },
                        },
                    ],
                    "blocks_de": [
                        {
                            "id": "323a4398-5412-4a5d-8c53-c57060db0d77",
                            "type": "hero",
                            "props": {
                                "kicker": "Willkommen bei",
                                "title": "Unserem Gemeinschaftsraum",
                                "subtitle": "Ein lokaler Veranstaltungsort, der Menschen durch Musik, Kunst und großartige Getränke zusammenbringt. Erleben Sie die lebendige Atmosphäre unseres Nachbarschaftstreffpunkts.",
                                "background_image": "",
                                "overlay": 0.45,
                                "alignment": "center",
                                "actions": [],
                            },
                        },
                        {
                            "id": "50249da0-a80a-4242-b9ff-03d08f54dcaa",
                            "type": "contact",
                            "props": {"show_social": True},
                        },
                        {
                            "id": "efcad5d3-7731-4bf8-9596-23fafd4f21c6",
                            "type": "menu",
                            "props": {
                                "title": "Menü-Highlights",
                                "subtitle": "Entdecken Sie unsere Auswahl an Getränken und Snacks",
                                "category_slugs": [],
                            },
                        },
                        {
                            "id": "214f2243-6f37-4f4a-bba2-ef132a1072c6",
                            "type": "footer",
                            "props": {
                                "brand_name": "",
                                "brand_tagline": "",
                                "brand_logo": "",
                                "address_html": "",
                                "links": [],
                                "legal": [],
                                "social_links": [],
                                "show_social": True,
                            },
                        },
                    ],
                    "blocks_fr": [
                        {
                            "id": "323a4398-5412-4a5d-8c53-c57060db0d77",
                            "type": "hero",
                            "props": {
                                "kicker": "Bienvenue à",
                                "title": "Notre Espace Communautaire",
                                "subtitle": "Un lieu local qui rassemble les gens autour de la musique, de l'art et d'excellentes boissons. Découvrez l'atmosphère vibrante de notre point de rencontre de quartier.",
                                "background_image": "",
                                "overlay": 0.45,
                                "alignment": "center",
                                "actions": [],
                            },
                        },
                        {
                            "id": "50249da0-a80a-4242-b9ff-03d08f54dcaa",
                            "type": "contact",
                            "props": {"show_social": True},
                        },
                        {
                            "id": "efcad5d3-7731-4bf8-9596-23fafd4f21c6",
                            "type": "menu",
                            "props": {
                                "title": "Points Forts du Menu",
                                "subtitle": "Découvrez notre sélection de boissons et collations",
                                "category_slugs": [],
                            },
                        },
                        {
                            "id": "214f2243-6f37-4f4a-bba2-ef132a1072c6",
                            "type": "footer",
                            "props": {
                                "brand_name": "",
                                "brand_tagline": "",
                                "brand_logo": "",
                                "address_html": "",
                                "links": [],
                                "legal": [],
                                "social_links": [],
                                "show_social": True,
                            },
                        },
                    ],
                },
                {
                    "title_en": "Menu",
                    "title_es": "Menú",
                    "title_de": "Speisekarte",
                    "title_fr": "Menu",
                    "slug_en": "menu",
                    "slug_es": "menu",
                    "slug_de": "speisekarte",
                    "slug_fr": "menu",
                    "summary_en": "Explore our selection of craft beers, cocktails, and delicious food options",
                    "summary_es": "Explora nuestra selección de cervezas artesanales, cócteles y deliciosas opciones de comida",
                    "summary_de": "Entdecken Sie unsere Auswahl an Craft-Bieren, Cocktails und köstlichen Speisen",
                    "summary_fr": "Découvrez notre sélection de bières artisanales, cocktails et délicieuses options alimentaires",
                    "body_en": "",
                    "body_es": "",
                    "body_de": "",
                    "body_fr": "",
                    "status": "published",
                    "is_visible": True,
                    "navigation_order": 1,
                    "show_navigation_bar": True,
                    "custom_nav_items": [],
                    "render_body_only": False,
                    "blocks_en": [
                        {
                            "id": "e74a4217-32ce-4cad-bc85-638cb1ac6f77",
                            "type": "hero",
                            "props": {
                                "kicker": "Food & Drinks",
                                "title": "Our Menu",
                                "subtitle": "From craft beers to signature cocktails and tasty bites, we've got something for everyone",
                                "background_image": "",
                                "overlay": 0.45,
                                "alignment": "center",
                                "actions": [],
                            },
                        },
                        {
                            "id": "62a53c26-88bf-4659-8765-70485dde00fe",
                            "type": "menu",
                            "props": {
                                "title": "Menu Highlights",
                                "subtitle": "Featured items from our kitchen and bar",
                                "category_slugs": [],
                            },
                        },
                    ],
                    "blocks_es": [
                        {
                            "id": "e74a4217-32ce-4cad-bc85-638cb1ac6f77",
                            "type": "hero",
                            "props": {
                                "kicker": "Comida y Bebidas",
                                "title": "Nuestro Menú",
                                "subtitle": "Desde cervezas artesanales hasta cócteles exclusivos y bocadillos sabrosos, tenemos algo para todos",
                                "background_image": "",
                                "overlay": 0.45,
                                "alignment": "center",
                                "actions": [],
                            },
                        },
                        {
                            "id": "62a53c26-88bf-4659-8765-70485dde00fe",
                            "type": "menu",
                            "props": {
                                "title": "Destacados del Menú",
                                "subtitle": "Artículos destacados de nuestra cocina y bar",
                                "category_slugs": [],
                            },
                        },
                    ],
                    "blocks_de": [
                        {
                            "id": "e74a4217-32ce-4cad-bc85-638cb1ac6f77",
                            "type": "hero",
                            "props": {
                                "kicker": "Essen & Getränke",
                                "title": "Unsere Speisekarte",
                                "subtitle": "Von Craft-Bieren bis zu Signature-Cocktails und leckeren Häppchen haben wir für jeden etwas",
                                "background_image": "",
                                "overlay": 0.45,
                                "alignment": "center",
                                "actions": [],
                            },
                        },
                        {
                            "id": "62a53c26-88bf-4659-8765-70485dde00fe",
                            "type": "menu",
                            "props": {
                                "title": "Menü-Highlights",
                                "subtitle": "Ausgewählte Artikel aus unserer Küche und Bar",
                                "category_slugs": [],
                            },
                        },
                    ],
                    "blocks_fr": [
                        {
                            "id": "e74a4217-32ce-4cad-bc85-638cb1ac6f77",
                            "type": "hero",
                            "props": {
                                "kicker": "Nourriture & Boissons",
                                "title": "Notre Menu",
                                "subtitle": "Des bières artisanales aux cocktails signature et aux bouchées savoureuses, nous avons quelque chose pour tout le monde",
                                "background_image": "",
                                "overlay": 0.45,
                                "alignment": "center",
                                "actions": [],
                            },
                        },
                        {
                            "id": "62a53c26-88bf-4659-8765-70485dde00fe",
                            "type": "menu",
                            "props": {
                                "title": "Points Forts du Menu",
                                "subtitle": "Articles en vedette de notre cuisine et bar",
                                "category_slugs": [],
                            },
                        },
                    ],
                },
                {
                    "title_en": "About",
                    "title_es": "Acerca de",
                    "title_de": "Über uns",
                    "title_fr": "À propos",
                    "slug_en": "about",
                    "slug_es": "acerca-de",
                    "slug_de": "uber-uns",
                    "slug_fr": "a-propos",
                    "summary_en": "Learn about our venue's history and mission to support local artists and community",
                    "summary_es": "Conoce la historia de nuestro local y nuestra misión de apoyar a los artistas locales y la comunidad",
                    "summary_de": "Erfahren Sie mehr über die Geschichte unseres Veranstaltungsortes und unsere Mission, lokale Künstler und die Gemeinschaft zu unterstützen",
                    "summary_fr": "Découvrez l'histoire de notre lieu et notre mission de soutenir les artistes locaux et la communauté",
                    "body_en": "<h2>Our Story</h2><p>Welcome to our community-driven venue, where music, art, and great conversations come together. Since opening our doors, we've been dedicated to creating a welcoming space for local artists, musicians, and community members to connect and collaborate.</p><h3>Our Mission</h3><p>We believe in the power of community and the arts. Our mission is to provide a platform for emerging artists while offering a comfortable space for everyone to enjoy quality drinks and entertainment.</p><h3>What We Offer</h3><ul><li>Live music performances</li><li>Art exhibitions</li><li>Community events</li><li>Craft beer selection</li><li>Signature cocktails</li><li>Delicious food menu</li></ul>",
                    "body_es": "<h2>Nuestra Historia</h2><p>Bienvenido a nuestro local impulsado por la comunidad, donde la música, el arte y las grandes conversaciones se unen. Desde que abrimos nuestras puertas, nos hemos dedicado a crear un espacio acogedor para que artistas locales, músicos y miembros de la comunidad se conecten y colaboren.</p><h3>Nuestra Misión</h3><p>Creemos en el poder de la comunidad y las artes. Nuestra misión es proporcionar una plataforma para artistas emergentes mientras ofrecemos un espacio cómodo para que todos disfruten de bebidas de calidad y entretenimiento.</p><h3>Lo Que Ofrecemos</h3><ul><li>Actuaciones de música en vivo</li><li>Exposiciones de arte</li><li>Eventos comunitarios</li><li>Selección de cervezas artesanales</li><li>Cócteles exclusivos</li><li>Menú de comida deliciosa</li></ul>",
                    "body_de": "<h2>Unsere Geschichte</h2><p>Willkommen in unserem gemeinschaftsorientierten Veranstaltungsort, wo Musik, Kunst und tolle Gespräche zusammenkommen. Seit wir unsere Türen geöffnet haben, sind wir bestrebt, einen einladenden Raum für lokale Künstler, Musiker und Gemeindemitglieder zu schaffen, um sich zu vernetzen und zusammenzuarbeiten.</p><h3>Unsere Mission</h3><p>Wir glauben an die Kraft der Gemeinschaft und der Künste. Unsere Mission ist es, eine Plattform für aufstrebende Künstler zu bieten und gleichzeitig einen komfortablen Raum für alle zu schaffen, um hochwertige Getränke und Unterhaltung zu genießen.</p><h3>Was Wir Anbieten</h3><ul><li>Live-Musikauftritte</li><li>Kunstausstellungen</li><li>Gemeinschaftsveranstaltungen</li><li>Craft-Beer-Auswahl</li><li>Signature-Cocktails</li><li>Köstliches Speisemenü</li></ul>",
                    "body_fr": "<h2>Notre Histoire</h2><p>Bienvenue dans notre lieu axé sur la communauté, où la musique, l'art et les grandes conversations se rejoignent. Depuis l'ouverture de nos portes, nous nous sommes consacrés à créer un espace accueillant pour que les artistes locaux, les musiciens et les membres de la communauté se connectent et collaborent.</p><h3>Notre Mission</h3><p>Nous croyons au pouvoir de la communauté et des arts. Notre mission est de fournir une plateforme pour les artistes émergents tout en offrant un espace confortable pour que tout le monde puisse profiter de boissons de qualité et de divertissement.</p><h3>Ce Que Nous Offrons</h3><ul><li>Performances de musique live</li><li>Expositions d'art</li><li>Événements communautaires</li><li>Sélection de bières artisanales</li><li>Cocktails signature</li><li>Menu de nourriture délicieux</li></ul>",
                    "status": "published",
                    "is_visible": True,
                    "navigation_order": 2,
                    "show_navigation_bar": True,
                    "custom_nav_items": [],
                    "render_body_only": False,
                    "blocks_en": [],
                    "blocks_es": [],
                    "blocks_de": [],
                    "blocks_fr": [],
                },
                {
                    "title_en": "Contact",
                    "title_es": "Contacto",
                    "title_de": "Kontakt",
                    "title_fr": "Contact",
                    "slug_en": "contact",
                    "slug_es": "contacto",
                    "slug_de": "kontakt",
                    "slug_fr": "contact",
                    "summary_en": "Get in touch with us for bookings, inquiries, or just to say hello",
                    "summary_es": "Ponte en contacto con nosotros para reservas, consultas o simplemente saludar",
                    "summary_de": "Kontaktieren Sie uns für Buchungen, Anfragen oder einfach nur zum Hallo sagen",
                    "summary_fr": "Contactez-nous pour des réservations, des demandes ou simplement pour dire bonjour",
                    "body_en": "<h2>Get in Touch</h2><p>We'd love to hear from you! Whether you're interested in booking an event, have questions about our menu, or just want to learn more about our community space, don't hesitate to reach out.</p><h3>Visit Us</h3><p><strong>Address:</strong> 123 Main Street, Your City, ST 12345<br><strong>Hours:</strong> Tue-Thu: 5PM-11PM, Fri-Sat: 5PM-2AM, Sun: 3PM-10PM</p><h3>Contact Information</h3><p><strong>Phone:</strong> (555) 123-4567<br><strong>Email:</strong> info@example.com</p><h3>Follow Us</h3><p>Stay updated on events and specials by following us on social media!</p>",
                    "body_es": "<h2>Ponte en Contacto</h2><p>¡Nos encantaría saber de ti! Ya sea que estés interesado en reservar un evento, tengas preguntas sobre nuestro menú o simplemente quieras saber más sobre nuestro espacio comunitario, no dudes en contactarnos.</p><h3>Visítanos</h3><p><strong>Dirección:</strong> Calle Principal 123, Tu Ciudad, ST 12345<br><strong>Horario:</strong> Mar-Jue: 5PM-11PM, Vie-Sáb: 5PM-2AM, Dom: 3PM-10PM</p><h3>Información de Contacto</h3><p><strong>Teléfono:</strong> (555) 123-4567<br><strong>Correo:</strong> info@example.com</p><h3>Síguenos</h3><p>¡Mantente actualizado sobre eventos y ofertas especiales siguiéndonos en las redes sociales!</p>",
                    "body_de": "<h2>Kontaktieren Sie Uns</h2><p>Wir würden uns freuen, von Ihnen zu hören! Egal, ob Sie an einer Veranstaltungsbuchung interessiert sind, Fragen zu unserer Speisekarte haben oder einfach mehr über unseren Gemeinschaftsraum erfahren möchten, zögern Sie nicht, uns zu kontaktieren.</p><h3>Besuchen Sie Uns</h3><p><strong>Adresse:</strong> Hauptstraße 123, Ihre Stadt, ST 12345<br><strong>Öffnungszeiten:</strong> Di-Do: 17-23 Uhr, Fr-Sa: 17-2 Uhr, So: 15-22 Uhr</p><h3>Kontaktinformationen</h3><p><strong>Telefon:</strong> (555) 123-4567<br><strong>E-Mail:</strong> info@example.com</p><h3>Folgen Sie Uns</h3><p>Bleiben Sie über Veranstaltungen und Sonderangebote auf dem Laufenden, indem Sie uns in den sozialen Medien folgen!</p>",
                    "body_fr": "<h2>Contactez-Nous</h2><p>Nous serions ravis d'avoir de vos nouvelles! Que vous soyez intéressé par la réservation d'un événement, que vous ayez des questions sur notre menu ou que vous souhaitiez simplement en savoir plus sur notre espace communautaire, n'hésitez pas à nous contacter.</p><h3>Visitez-Nous</h3><p><strong>Adresse:</strong> 123 Rue Principale, Votre Ville, ST 12345<br><strong>Heures:</strong> Mar-Jeu: 17h-23h, Ven-Sam: 17h-2h, Dim: 15h-22h</p><h3>Informations de Contact</h3><p><strong>Téléphone:</strong> (555) 123-4567<br><strong>E-mail:</strong> info@example.com</p><h3>Suivez-Nous</h3><p>Restez informé des événements et des offres spéciales en nous suivant sur les réseaux sociaux!</p>",
                    "status": "published",
                    "is_visible": True,
                    "navigation_order": 3,
                    "show_navigation_bar": True,
                    "custom_nav_items": [],
                    "render_body_only": False,
                    "blocks_en": [],
                    "blocks_es": [],
                    "blocks_de": [],
                    "blocks_fr": [],
                },
                {
                    "title_en": "Events",
                    "title_es": "Eventos",
                    "title_de": "Veranstaltungen",
                    "title_fr": "Événements",
                    "slug_en": "events",
                    "slug_es": "eventos",
                    "slug_de": "veranstaltungen",
                    "slug_fr": "evenements",
                    "summary_en": "Check out our upcoming events and book your spot for the next show",
                    "summary_es": "Consulta nuestros próximos eventos y reserva tu lugar para el próximo espectáculo",
                    "summary_de": "Schauen Sie sich unsere kommenden Veranstaltungen an und buchen Sie Ihren Platz für die nächste Show",
                    "summary_fr": "Découvrez nos événements à venir et réservez votre place pour le prochain spectacle",
                    "body_en": "<h2>Upcoming Events</h2><p>Join us for an exciting lineup of live music, DJ nights, comedy shows, and community events. Check our calendar regularly for the latest updates and special performances.</p><h3>Event Types</h3><ul><li>Live Music - Local and touring bands</li><li>DJ Nights - Electronic and dance music</li><li>Comedy Open Mic - Weekly comedy showcase</li><li>Art Exhibitions - Local artist displays</li><li>Community Gatherings - Special themed events</li></ul><h3>Booking Information</h3><p>Interested in performing or hosting an event? Contact us at events@example.com with details about your act or event idea.</p>",
                    "body_es": "<h2>Próximos Eventos</h2><p>Únete a nosotros para una emocionante programación de música en vivo, noches de DJ, espectáculos de comedia y eventos comunitarios. Consulta nuestro calendario regularmente para las últimas actualizaciones y actuaciones especiales.</p><h3>Tipos de Eventos</h3><ul><li>Música en Vivo - Bandas locales y de gira</li><li>Noches de DJ - Música electrónica y dance</li><li>Micrófono Abierto de Comedia - Showcase de comedia semanal</li><li>Exposiciones de Arte - Exhibiciones de artistas locales</li><li>Reuniones Comunitarias - Eventos temáticos especiales</li></ul><h3>Información de Reservas</h3><p>¿Interesado en actuar o organizar un evento? Contáctanos en events@example.com con detalles sobre tu acto o idea de evento.</p>",
                    "body_de": "<h2>Kommende Veranstaltungen</h2><p>Nehmen Sie teil an unserer aufregenden Reihe von Live-Musik, DJ-Abenden, Comedy-Shows und Community-Events. Schauen Sie regelmäßig in unseren Kalender für die neuesten Updates und besondere Auftritte.</p><h3>Veranstaltungstypen</h3><ul><li>Live-Musik - Lokale und tourende Bands</li><li>DJ-Abende - Elektronische und Tanzmusik</li><li>Comedy Open Mic - Wöchentliche Comedy-Showcase</li><li>Kunstausstellungen - Lokale Künstlerausstellungen</li><li>Community-Treffen - Spezielle thematische Events</li></ul><h3>Buchungsinformationen</h3><p>Interessiert daran, aufzutreten oder ein Event zu veranstalten? Kontaktieren Sie uns unter events@example.com mit Details über Ihren Auftritt oder Ihre Event-Idee.</p>",
                    "body_fr": "<h2>Événements à Venir</h2><p>Rejoignez-nous pour une programmation passionnante de musique live, soirées DJ, spectacles de comédie et événements communautaires. Consultez régulièrement notre calendrier pour les dernières mises à jour et performances spéciales.</p><h3>Types d'Événements</h3><ul><li>Musique Live - Groupes locaux et en tournée</li><li>Soirées DJ - Musique électronique et dance</li><li>Micro Ouvert Comédie - Showcase de comédie hebdomadaire</li><li>Expositions d'Art - Présentations d'artistes locaux</li><li>Rassemblements Communautaires - Événements thématiques spéciaux</li></ul><h3>Informations de Réservation</h3><p>Intéressé à performer ou organiser un événement? Contactez-nous à events@example.com avec des détails sur votre acte ou votre idée d'événement.</p>",
                    "status": "published",
                    "is_visible": True,
                    "navigation_order": 4,
                    "show_navigation_bar": True,
                    "custom_nav_items": [],
                    "render_body_only": False,
                    "blocks_en": [],
                    "blocks_es": [],
                    "blocks_de": [],
                    "blocks_fr": [],
                },
                {
                    "title_en": "Login",
                    "title_es": "Iniciar sesión",
                    "title_de": "Anmelden",
                    "title_fr": "Connexion",
                    "slug_en": "login",
                    "slug_es": "login",
                    "slug_de": "login",
                    "slug_fr": "login",
                    "summary_en": "Member login page",
                    "summary_es": "Página de inicio de sesión de miembros",
                    "summary_de": "Mitglieder-Anmeldeseite",
                    "summary_fr": "Page de connexion des membres",
                    "body_en": "",
                    "body_es": "",
                    "body_de": "",
                    "body_fr": "",
                    "status": "published",
                    "navigation_order": 99,
                    "show_navigation_bar": True,
                    "custom_nav_items": [],
                    "render_body_only": False,
                    "blocks_en": [],
                    "blocks_es": [],
                    "blocks_de": [],
                    "blocks_fr": [],
                },
            ]

            for page_data in pages_data:
                # Set created_by and updated_by if admin user exists
                if admin_user:
                    page_data["created_by"] = admin_user
                    page_data["updated_by"] = admin_user

                # Set published_at for published pages
                if page_data["status"] == "published":
                    page_data["published_at"] = timezone.now()

                # Create or update the page using English slug as the unique key
                slug_en = page_data.get("slug_en")
                page, created = Page.objects.update_or_create(slug_en=slug_en, defaults=page_data)

                if created:
                    self.stdout.write(f"  ✓ Created page: {page.title}")
                else:
                    self.stdout.write(f"  ✓ Updated page: {page.title}")

            self.stdout.write(self.style.SUCCESS("  ✓ Successfully seeded pages"))
        except ImportError:
            self.stdout.write(self.style.WARNING("  ⊘ Pages app not available"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Error seeding pages: {e}"))

    def seed_events(self):
        """Create sample events."""
        self.stdout.write("Seeding events...")

        try:
            from app.events.models import Event, EventCategory

            # Create categories with multilingual support
            categories_data = [
                {
                    "name_en": "Live Music",
                    "name_es": "Música en Vivo",
                    "name_de": "Live-Musik",
                    "name_fr": "Musique Live",
                    "slug_en": "live-music",
                    "slug_es": "musica-en-vivo",
                    "slug_de": "live-musik",
                    "slug_fr": "musique-live",
                },
                {
                    "name_en": "DJ Night",
                    "name_es": "Noche de DJ",
                    "name_de": "DJ-Nacht",
                    "name_fr": "Soirée DJ",
                    "slug_en": "dj-night",
                    "slug_es": "noche-de-dj",
                    "slug_de": "dj-nacht",
                    "slug_fr": "soiree-dj",
                },
                {
                    "name_en": "Comedy",
                    "name_es": "Comedia",
                    "name_de": "Comedy",
                    "name_fr": "Comédie",
                    "slug_en": "comedy",
                    "slug_es": "comedia",
                    "slug_de": "comedy",
                    "slug_fr": "comedie",
                },
                {
                    "name_en": "Art Show",
                    "name_es": "Exposición de Arte",
                    "name_de": "Kunstausstellung",
                    "name_fr": "Exposition d'Art",
                    "slug_en": "art-show",
                    "slug_es": "exposicion-de-arte",
                    "slug_de": "kunstausstellung",
                    "slug_fr": "exposition-art",
                },
                {
                    "name_en": "Private Event",
                    "name_es": "Evento Privado",
                    "name_de": "Private Veranstaltung",
                    "name_fr": "Événement Privé",
                    "slug_en": "private-event",
                    "slug_es": "evento-privado",
                    "slug_de": "private-veranstaltung",
                    "slug_fr": "evenement-prive",
                },
            ]

            categories = {}
            for cat_data in categories_data:
                cat, _ = EventCategory.objects.update_or_create(
                    slug_en=cat_data["slug_en"], defaults=cat_data
                )
                categories[cat_data["slug_en"]] = cat

            # Create events with multilingual support
            now = timezone.now()
            events_data = [
                {
                    "title_en": "Friday Night Jazz",
                    "title_es": "Jazz del Viernes por la Noche",
                    "title_de": "Freitag Abend Jazz",
                    "title_fr": "Jazz du Vendredi Soir",
                    "slug_en": "friday-night-jazz",
                    "slug_es": "jazz-viernes-noche",
                    "slug_de": "freitag-abend-jazz",
                    "slug_fr": "jazz-vendredi-soir",
                    "teaser_en": "Smooth jazz evening with local artists",
                    "teaser_es": "Noche de jazz suave con artistas locales",
                    "teaser_de": "Sanfter Jazzabend mit lokalen Künstlern",
                    "teaser_fr": "Soirée jazz en douceur avec des artistes locaux",
                    "description_public_en": "Join us for an evening of smooth jazz featuring local artists.",
                    "description_public_es": "Únete a nosotros para una noche de jazz suave con artistas locales.",
                    "description_public_de": "Begleiten Sie uns zu einem Abend mit sanftem Jazz mit lokalen Künstlern.",
                    "description_public_fr": "Rejoignez-nous pour une soirée de jazz en douceur avec des artistes locaux.",
                    "status": Event.Status.PUBLISHED,
                    "starts_at": now + timedelta(days=5, hours=20),
                    "ends_at": now + timedelta(days=5, hours=23),
                    "doors_at": now + timedelta(days=5, hours=19, minutes=30),
                    "event_type": Event.EventType.PUBLIC,
                },
                {
                    "title_en": "Weekend DJ Bash",
                    "title_es": "Fiesta DJ del Fin de Semana",
                    "title_de": "Wochenende DJ Party",
                    "title_fr": "Soirée DJ du Week-end",
                    "slug_en": "weekend-dj-bash",
                    "slug_es": "fiesta-dj-fin-de-semana",
                    "slug_de": "wochenende-dj-party",
                    "slug_fr": "soiree-dj-weekend",
                    "teaser_en": "Weekend dance party with resident DJs",
                    "teaser_es": "Fiesta de baile del fin de semana con DJs residentes",
                    "teaser_de": "Wochenend-Tanzparty mit Resident-DJs",
                    "teaser_fr": "Soirée dansante du week-end avec DJs résidents",
                    "description_public_en": "Dance the night away with our resident DJs!",
                    "description_public_es": "¡Baila toda la noche con nuestros DJs residentes!",
                    "description_public_de": "Tanzen Sie die ganze Nacht mit unseren Resident-DJs!",
                    "description_public_fr": "Dansez toute la nuit avec nos DJs résidents!",
                    "status": Event.Status.PUBLISHED,
                    "starts_at": now + timedelta(days=7, hours=22),
                    "ends_at": now + timedelta(days=8, hours=2),
                    "doors_at": now + timedelta(days=7, hours=21, minutes=30),
                    "event_type": Event.EventType.PUBLIC,
                },
                {
                    "title_en": "Comedy Open Mic",
                    "title_es": "Micrófono Abierto de Comedia",
                    "title_de": "Comedy Open Mic",
                    "title_fr": "Micro Ouvert Comédie",
                    "slug_en": "comedy-open-mic",
                    "slug_es": "microfono-abierto-comedia",
                    "slug_de": "comedy-open-mic",
                    "slug_fr": "micro-ouvert-comedie",
                    "teaser_en": "Weekly comedy showcase",
                    "teaser_es": "Espectáculo de comedia semanal",
                    "teaser_de": "Wöchentliche Comedy-Show",
                    "teaser_fr": "Spectacle de comédie hebdomadaire",
                    "description_public_en": "Laugh out loud at our weekly comedy open mic night.",
                    "description_public_es": "Ríete a carcajadas en nuestra noche semanal de micrófono abierto de comedia.",
                    "description_public_de": "Lachen Sie laut bei unserer wöchentlichen Comedy-Open-Mic-Nacht.",
                    "description_public_fr": "Riez aux éclats lors de notre soirée micro ouvert comédie hebdomadaire.",
                    "status": Event.Status.PUBLISHED,
                    "starts_at": now + timedelta(days=3, hours=19),
                    "ends_at": now + timedelta(days=3, hours=22),
                    "doors_at": now + timedelta(days=3, hours=18, minutes=30),
                    "event_type": Event.EventType.PUBLIC,
                },
            ]

            for event_data in events_data:
                event, created = Event.objects.update_or_create(
                    slug_en=event_data["slug_en"], defaults=event_data
                )
                if created:
                    # Add categories to event
                    if "jazz" in event_data["slug_en"]:
                        event.categories.add(categories["live-music"])
                    elif "dj" in event_data["slug_en"]:
                        event.categories.add(categories["dj-night"])
                    elif "comedy" in event_data["slug_en"]:
                        event.categories.add(categories["comedy"])

            self.stdout.write(self.style.SUCCESS("  ✓ Created sample events"))
        except ImportError:
            self.stdout.write(self.style.WARNING("  ⊘ Events app not available"))

    def seed_menu_items(self):
        """Create sample menu items."""
        self.stdout.write("Seeding menu items...")

        try:
            from app.menu.models import Category, Item, ItemVariant, Unit

            # Get or create units with multilingual support
            unit_ml, _ = Unit.objects.get_or_create(
                code="mL",
                defaults={
                    "display_en": "Milliliters",
                    "display_es": "Mililitros",
                    "display_de": "Milliliter",
                    "display_fr": "Millilitres",
                    "kind": "volume",
                },
            )
            unit_l, _ = Unit.objects.get_or_create(
                code="L",
                defaults={
                    "display_en": "Liters",
                    "display_es": "Litros",
                    "display_de": "Liter",
                    "display_fr": "Litres",
                    "kind": "volume",
                },
            )
            unit_pcs, _ = Unit.objects.get_or_create(
                code="pcs",
                defaults={
                    "display_en": "Pieces",
                    "display_es": "Piezas",
                    "display_de": "Stück",
                    "display_fr": "Pièces",
                    "kind": "count",
                },
            )

            # Get or create root categories with multilingual support
            drinks_cat, _ = Category.objects.update_or_create(
                slug_en="drinks",
                defaults={
                    "name_en": "Drinks",
                    "name_es": "Bebidas",
                    "name_de": "Getränke",
                    "name_fr": "Boissons",
                    "slug_en": "drinks",
                    "slug_es": "bebidas",
                    "slug_de": "getranke",
                    "slug_fr": "boissons",
                    "parent": None,
                },
            )
            food_cat, _ = Category.objects.update_or_create(
                slug_en="food",
                defaults={
                    "name_en": "Food",
                    "name_es": "Comida",
                    "name_de": "Essen",
                    "name_fr": "Nourriture",
                    "slug_en": "food",
                    "slug_es": "comida",
                    "slug_de": "essen",
                    "slug_fr": "nourriture",
                    "parent": None,
                },
            )

            # Create subcategories with multilingual support
            beer_cat, _ = Category.objects.update_or_create(
                slug_en="beer",
                defaults={
                    "name_en": "Beer",
                    "name_es": "Cerveza",
                    "name_de": "Bier",
                    "name_fr": "Bière",
                    "slug_en": "beer",
                    "slug_es": "cerveza",
                    "slug_de": "bier",
                    "slug_fr": "biere",
                    "parent": drinks_cat,
                },
            )
            cocktails_cat, _ = Category.objects.update_or_create(
                slug_en="cocktails",
                defaults={
                    "name_en": "Cocktails",
                    "name_es": "Cócteles",
                    "name_de": "Cocktails",
                    "name_fr": "Cocktails",
                    "slug_en": "cocktails",
                    "slug_es": "cocteles",
                    "slug_de": "cocktails",
                    "slug_fr": "cocktails",
                    "parent": drinks_cat,
                },
            )
            snacks_cat, _ = Category.objects.update_or_create(
                slug_en="snacks",
                defaults={
                    "name_en": "Snacks",
                    "name_es": "Aperitivos",
                    "name_de": "Snacks",
                    "name_fr": "Snacks",
                    "slug_en": "snacks",
                    "slug_es": "aperitivos",
                    "slug_de": "snacks",
                    "slug_fr": "snacks",
                    "parent": food_cat,
                },
            )

            # Create menu items
            items_data = [
                {
                    "name_en": "House Lager",
                    "slug_en": "house-lager",
                    "category": beer_cat,
                    "description_en": "Crisp and refreshing local lager",
                },
                {
                    "name_en": "IPA",
                    "slug_en": "ipa",
                    "category": beer_cat,
                    "description_en": "Hoppy India Pale Ale",
                },
                {
                    "name_en": "Old Fashioned",
                    "slug_en": "old-fashioned",
                    "category": cocktails_cat,
                    "description_en": "Classic whiskey cocktail",
                },
                {
                    "name_en": "Margarita",
                    "slug_en": "margarita",
                    "category": cocktails_cat,
                    "description_en": "Fresh lime margarita on the rocks",
                },
                {
                    "name_en": "Nachos",
                    "slug_en": "nachos",
                    "category": snacks_cat,
                    "description_en": "Tortilla chips with cheese, jalapeños, and salsa",
                },
                {
                    "name_en": "Wings",
                    "slug_en": "wings",
                    "category": snacks_cat,
                    "description_en": "Buffalo wings with ranch dressing",
                },
            ]

            for item_data in items_data:
                # Use slug_en as unique identifier
                slug_en = item_data.pop("slug_en")
                item, created = Item.objects.update_or_create(slug_en=slug_en, defaults=item_data)
                if created:
                    # Create variants with prices
                    if "Lager" in item.name:
                        ItemVariant.objects.create(
                            item=item,
                            label="Small",
                            quantity=Decimal("0.330"),
                            unit=unit_ml,
                            price=Decimal("6.50"),
                        )
                        ItemVariant.objects.create(
                            item=item,
                            label="Large",
                            quantity=Decimal("0.5"),
                            unit=unit_l,
                            price=Decimal("3.50"),
                        )
                    elif "IPA" in item.name:
                        ItemVariant.objects.create(
                            item=item,
                            label="Pint",
                            quantity=Decimal("0.5"),
                            unit=unit_l,
                            price=Decimal("7.50"),
                        )
                    elif "Old Fashioned" in item.name:
                        ItemVariant.objects.create(
                            item=item,
                            label="Standard",
                            quantity=Decimal("1"),
                            unit=unit_pcs,
                            price=Decimal("12.00"),
                        )
                    elif "Margarita" in item.name:
                        ItemVariant.objects.create(
                            item=item,
                            label="Regular",
                            quantity=Decimal("0.35"),
                            unit=unit_l,
                            price=Decimal("10.00"),
                        )
                    elif "Nachos" in item.name:
                        ItemVariant.objects.create(
                            item=item,
                            label="Regular",
                            quantity=Decimal("1"),
                            unit=unit_pcs,
                            price=Decimal("8.50"),
                        )
                    elif "Wings" in item.name:
                        ItemVariant.objects.create(
                            item=item,
                            label="Order",
                            quantity=Decimal("1"),
                            unit=unit_pcs,
                            price=Decimal("11.00"),
                        )

            self.stdout.write(self.style.SUCCESS("  ✓ Created sample menu items"))
        except ImportError:
            self.stdout.write(self.style.WARNING("  ⊘ Menu app not available"))

    def seed_merch(self):
        """Create sample merchandise."""
        self.stdout.write("Seeding merchandise...")

        try:
            from app.merch.models import Category, Product

            # Create categories
            apparel_cat, _ = Category.objects.get_or_create(
                slug="apparel", defaults={"name": "Apparel"}
            )
            accessories_cat, _ = Category.objects.get_or_create(
                slug="accessories", defaults={"name": "Accessories"}
            )

            # Create products
            products_data = [
                {
                    "name": "Venue T-Shirt",
                    "slug": "venue-tshirt",
                    "category": apparel_cat,
                    "base_price": Decimal("25.00"),
                    "description": "Classic black t-shirt with venue logo",
                    "visible_public": True,
                },
                {
                    "name": "Hoodie",
                    "slug": "hoodie",
                    "category": apparel_cat,
                    "base_price": Decimal("45.00"),
                    "description": "Cozy hoodie perfect for cold nights",
                    "visible_public": True,
                },
                {
                    "name": "Sticker Pack",
                    "slug": "sticker-pack",
                    "category": accessories_cat,
                    "base_price": Decimal("5.00"),
                    "description": "Set of 5 vinyl stickers",
                    "visible_public": True,
                },
            ]

            for product_data in products_data:
                Product.objects.get_or_create(slug=product_data["slug"], defaults=product_data)

            self.stdout.write(self.style.SUCCESS("  ✓ Created sample merchandise"))
        except ImportError:
            self.stdout.write(self.style.WARNING("  ⊘ Merch app not available"))

    def seed_bands(self):
        """Create sample bands/performers."""
        self.stdout.write("Seeding bands...")

        try:
            from app.bands.models import Band

            bands_data = [
                {
                    "name": "The Local Heroes",
                    "slug": "the-local-heroes",
                    "description": "Rock band from the neighborhood",
                    "performer_type": "band",
                    "contact_type": "email",
                    "contact_value": "bookings@localheroes.com",
                    "compensation_type": "door",
                    "entry_price": 15.00,
                    "is_published": True,
                },
                {
                    "name": "Jazz Collective",
                    "slug": "jazz-collective",
                    "description": "Smooth jazz ensemble",
                    "performer_type": "band",
                    "contact_type": "email",
                    "contact_value": "info@jazzcollective.com",
                    "compensation_type": "fixed",
                    "fee_amount": 250.00,
                    "is_published": True,
                },
                {
                    "name": "DJ Spinner",
                    "slug": "dj-spinner",
                    "description": "Electronic music DJ",
                    "performer_type": "dj",
                    "contact_type": "phone",
                    "contact_value": "+45 98 76 54 32",
                    "compensation_type": "door",
                    "entry_price": 20.00,
                    "is_published": True,
                },
            ]

            for band_data in bands_data:
                Band.objects.get_or_create(slug=band_data["slug"], defaults=band_data)

            self.stdout.write(self.style.SUCCESS("  ✓ Created sample bands"))
        except ImportError:
            self.stdout.write(self.style.WARNING("  ⊘ Bands app not available"))

    def seed_site_settings(self):
        """Create or update site settings."""
        self.stdout.write("Seeding site settings...")

        try:
            from app.setup.models import SiteSettings

            settings_obj, created = SiteSettings.objects.get_or_create(
                id=1,
                defaults={
                    "org_name": "Bar OS - Local Dev",
                    "contact_email": "info@example.com",
                    "contact_phone": "(555) 123-4567",
                    "address_street": "123 Main St",
                    "address_city": "Your City",
                    "address_postal_code": "12345",
                    "address_country": "ST",
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS("  ✓ Created site settings"))
            else:
                self.stdout.write(self.style.SUCCESS("  ✓ Site settings already exist"))
        except ImportError:
            self.stdout.write(self.style.WARNING("  ⊘ Setup app not available"))
