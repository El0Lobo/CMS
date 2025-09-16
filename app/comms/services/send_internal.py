
from django.utils import timezone
from django.db import transaction
from typing import List, Dict, Any, Optional

from app.comms.models import MessageThread, Message, InternalTarget, AudienceLink

@transaction.atomic
def post_internal(author, subject: str, body_text: str, targets: dict) -> MessageThread:
    """
    Create an internal thread and first message, attach targets.
    targets: dict with lists 'users', 'groups', 'badges' of ids
    """
    thread = MessageThread.objects.create(type=MessageThread.TYPE_INTERNAL, subject=subject or "")
    msg = Message.objects.create(
        thread=thread,
        direction=Message.DIR_INTERNAL,
        sender_user=author,
        sent_at=timezone.now(),
        body_text=body_text or "",
        body_html_sanitized="",
    )
    AudienceLink.objects.get_or_create(
        thread=thread, user_id=author.id, defaults={"source": "author"}
    )
    # Targets
    for uid in targets.get("users", []) or []:
        InternalTarget.objects.create(thread=thread, user_id=uid)
        AudienceLink.objects.create(thread=thread, user_id=uid, source="manual")
    for gid in targets.get("groups", []) or []:
        InternalTarget.objects.create(thread=thread, group_id=gid)
        AudienceLink.objects.create(thread=thread, group_id=gid, source="manual")
    for bid in targets.get("badges", []) or []:
        InternalTarget.objects.create(thread=thread, badge_id=bid)
        AudienceLink.objects.create(thread=thread, badge_id=bid, source="manual")

    return thread
