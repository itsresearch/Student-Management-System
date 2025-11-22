from django.db.models import QuerySet
from .models import Notification


def notification_context(request):
    """
    Provide unread notifications and count for the base layout.
    """
    if request.user.is_authenticated:
        unread_qs: QuerySet[Notification] = Notification.objects.filter(
            user=request.user, is_read=False
        ).order_by("-created_at")
        unread_list = list(unread_qs)
        return {
            "unread_notification": unread_list,
            "unread_notification_count": len(unread_list),
        }

    return {
        "unread_notification": [],
        "unread_notification_count": 0,
    }

