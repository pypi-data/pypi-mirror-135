# https://aio-pika.readthedocs.io/en/latest/rabbitmq-tutorial/1-introduction.html
import json

try:
    import aio_pika

    HAS_LIBS = (True,)
except ImportError:
    HAS_LIBS = False, "aio_pika is not available"


def __virtual__(hub):
    return HAS_LIBS


async def publish(hub, ctx, event):
    if not ctx and not ctx.connected:
        return

    encoded_event = json.dumps(event).encode()
    message = aio_pika.Message(encoded_event)

    async with ctx.connection.channel() as channel:
        for routing_key in ctx.channels:
            await channel.default_exchange.publish(message, routing_key=routing_key)
