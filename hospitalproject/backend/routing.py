from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

application = ProtocolTypeRouter({
    "websocket":URLRouter([

    ])
})
