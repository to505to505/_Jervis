"""
ASGI config for jervis project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.conf import settings
from aiohttp import web

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jervis.settings')
application = get_asgi_application()

# if settings.DEBUG:
#     app = web.Application()
#     app.add_routes([web.get('/', handler)])
#     web.run_app(app)
