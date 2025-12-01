from django.db import transaction
from django.utils import timezone

from app.comms.models import AudienceLink, InternalTarget, Message, MessageThread


@transaction.atomic
def post_internal(author, subject: str, body_text: str, targets: dict) -> MessageThread:
    """
    Create an internal thread and first message, attach targets.
    targets: dict with lists 'users', 'groups', 'badges' of ids
    """
    normalized_subject = subject or ""
    username = getattr(author, "username", "") or ""
    system_sender = username.lower() == "cliadmin"

    thread = None
    if system_sender:
        thread = (
            MessageThread.objects.filter(
                type=MessageThread.TYPE_INTERNAL, subject=normalized_subject
            )
            .order_by("-last_activity_at")
            .first()
        )
    if not thread:
        thread = MessageThread.objects.create(
            type=MessageThread.TYPE_INTERNAL, subject=normalized_subject
        )

    message_kwargs = dict(
        thread=thread,
        direction=Message.DIR_INTERNAL,
        sent_at=timezone.now(),
        body_text=body_text or "",
        body_html_sanitized="",
    )
    if system_sender:
        message_kwargs["sender_user"] = None
        message_kwargs["sender_display"] = "System"
    else:
        message_kwargs["sender_user"] = author

    Message.objects.create(**message_kwargs)

    if not system_sender and getattr(author, "id", None):
        AudienceLink.objects.get_or_create(
            thread=thread, user_id=author.id, defaults={"source": "author"}
        )

    # Targets
    for uid in targets.get("users", []) or []:
        InternalTarget.objects.get_or_create(thread=thread, user_id=uid)
        AudienceLink.objects.get_or_create(
            thread=thread, user_id=uid, defaults={"source": "manual"}
        )
    for gid in targets.get("groups", []) or []:
        InternalTarget.objects.get_or_create(thread=thread, group_id=gid)
        AudienceLink.objects.get_or_create(
            thread=thread, group_id=gid, defaults={"source": "manual"}
        )
    for bid in targets.get("badges", []) or []:
        InternalTarget.objects.get_or_create(thread=thread, badge_id=bid)
        AudienceLink.objects.get_or_create(
            thread=thread, badge_id=bid, defaults={"source": "manual"}
        )

    return thread
