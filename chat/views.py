from django.shortcuts import render
from .models import Message
from django.utils import timezone
from datetime import timedelta

def index(request):
    time_limit = timezone.now() - timedelta(hours=1)

    messages = Message.objects.filter(
        timestamp__gte=time_limit
    ).order_by("timestamp")

    return render(request, "chat/index.html", {
        "messages": messages
    })