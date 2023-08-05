try:
    import aio_pika

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


async def gather(hub, profiles):
    """
    Get profile names from an encrypted amqp credential files

    Example:

    .. code-block:: yaml

        pika:
          profile_name:
            host: localhost
            port: 5672
            ingress_channels:
              - channel1
              - channel2
    """
    sub_profiles = {}
    for (
        profile,
        ctx,
    ) in profiles.get("pika", {}).items():
        sub_profiles[profile] = {
            "connected": False,
            "channels": ctx.pop("ingress_channels", []),
            "connection": None,
        }

        hub.log.debug("connecting to rabbitmq server")
        try:
            sub_profiles[profile]["connection"] = await aio_pika.connect_robust(
                loop=hub.pop.Loop, **ctx
            )
            sub_profiles[profile]["connected"] = True
            hub.log.debug("connected to rabbitmq server")
        except Exception as err:
            hub.log.error("Could not connect to rabbitmq server")
            hub.log.error(str(err))

    return sub_profiles
