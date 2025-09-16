
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('from_name', models.CharField(blank=True, default='', max_length=120)),
                ('from_address', models.EmailField(blank=True, default='', max_length=254)),
                ('signature_html', models.TextField(blank=True, default='')),
                ('signature_text', models.TextField(blank=True, default='')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='MessageThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('internal', 'Internal'), ('email', 'Email')], default='internal', max_length=10)),
                ('subject', models.CharField(blank=True, default='', max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity_at', models.DateTimeField(auto_now=True)),
                ('has_attachments', models.BooleanField(default=False)),
                ('is_closed', models.BooleanField(default=False)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comms.mailaccount')),
            ],
            options={'ordering': ['-last_activity_at']},
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[('inbound', 'Inbound'), ('outbound', 'Outbound'), ('internal', 'Internal')], default='internal', max_length=10)),
                ('sender_display', models.CharField(blank=True, default='', max_length=200)),
                ('received_at', models.DateTimeField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('message_id', models.CharField(blank=True, default='', max_length=512)),
                ('in_reply_to', models.CharField(blank=True, default='', max_length=512)),
                ('references', models.TextField(blank=True, default='')),
                ('headers', models.JSONField(blank=True, null=True)),
                ('body_text', models.TextField(blank=True, default='')),
                ('body_html_sanitized', models.TextField(blank=True, default='')),
                ('has_trackers', models.BooleanField(default=False)),
                ('size_bytes', models.IntegerField(blank=True, null=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='comms.mailaccount')),
                ('sender_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='comms.messagethread')),
            ],
            options={'ordering': ['created_at']},
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('mime_type', models.CharField(blank=True, default='', max_length=100)),
                ('size_bytes', models.BigIntegerField(blank=True, null=True)),
                ('storage_path', models.CharField(blank=True, default='', max_length=500)),
                ('sha256', models.CharField(blank=True, default='', max_length=64)),
                ('is_inline', models.BooleanField(default=False)),
                ('content_id', models.CharField(blank=True, default='', max_length=255)),
                ('scan_status', models.CharField(choices=[('pending', 'Pending'), ('clean', 'Clean'), ('blocked', 'Blocked'), ('error', 'Error')], default='pending', max_length=16)),
                ('scan_detail', models.TextField(blank=True, default='')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='comms.message')),
            ],
        ),
        migrations.CreateModel(
            name='ReadReceipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_at', models.DateTimeField()),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_receipts', to='comms.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comms_reads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='readreceipt',
            constraint=models.UniqueConstraint(fields=('message', 'user'), name='comms_read_unique'),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField()),
                ('is_system', models.BooleanField(default=False)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comms.mailaccount')),
            ],
        ),
        migrations.AddConstraint(
            model_name='label',
            constraint=models.UniqueConstraint(fields=('account', 'slug'), name='comms_label_unique'),
        ),
        migrations.CreateModel(
            name='UserThreadState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archived', models.BooleanField(default=False)),
                ('starred', models.BooleanField(default=False)),
                ('last_read_at', models.DateTimeField(blank=True, null=True)),
                ('labels', models.ManyToManyField(blank=True, to='comms.label')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_states', to='comms.messagethread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread_states', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='userthreadstate',
            constraint=models.UniqueConstraint(fields=('thread', 'user'), name='comms_user_thread_state_unique'),
        ),
        migrations.CreateModel(
            name='AudienceLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(default='manual', max_length=20)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.badgedefinition')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audiences', to='comms.messagethread')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='audiencelink',
            constraint=models.UniqueConstraint(fields=('thread', 'badge', 'group', 'user'), name='comms_audience_unique_member'),
        ),
        migrations.CreateModel(
            name='InternalTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.badgedefinition')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internal_targets', to='comms.messagethread')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
