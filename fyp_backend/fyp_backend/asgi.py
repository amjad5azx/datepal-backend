"""
ASGI config for fyp_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from myapp.consumers.date_image_consumers import *
from myapp.consumers.date_name_consumers import *
from myapp.consumers.all_dates import *
from myapp.consumers.test_consumer import *
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fyp_backend.settings')

application = get_asgi_application()

ws_patterns=[
    path('ws/dates_image/',DateImageConsumer.as_asgi()),
    path('ws/dates_name/',DateNameConsumer.as_asgi()),
    path('ws/all_dates/',AllDatesConsumer.as_asgi()),
    path('ws/test/',TestConsumer.as_asgi()),
]

application=ProtocolTypeRouter({
    'websocket':URLRouter(ws_patterns)
})