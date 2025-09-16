from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
class Command(BaseCommand):
    help = "Create a DEV admin user quickly (DEBUG only)."
    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin")
        parser.add_argument("--email", default="admin@example.com")
        parser.add_argument("--password", default="admin123")
    def handle(self, *args, **opts):
        if not settings.DEBUG:
            self.stderr.write("Refusing to run while DEBUG=False"); return
        User = get_user_model()
        if User.objects.filter(username=opts["username"]).exists():
            self.stdout.write("User already exists."); return
        u = User.objects.create_superuser(opts["username"], opts["email"], opts["password"])
        self.stdout.write(f"Created superuser {u.username}")
