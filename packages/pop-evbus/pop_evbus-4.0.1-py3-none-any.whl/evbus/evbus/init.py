from typing import Any
from typing import Dict

STOP_ITERATION = object()


def __init__(hub):
    hub.evbus.STARTED = False
    hub.evbus.RUN_FOREVER = True
    for dyne in ("acct", "ingress", "output", "serialize"):
        hub.pop.sub.add(dyne_name=dyne)


async def start(hub, contexts: Dict[str, Dict[str, Any]]):
    hub.log.debug("Starting event bus")
    hub.evbus.STARTED = True

    # Initialize the queue in the current loop
    bus = await hub.evbus.broker.init()

    while hub.evbus.RUN_FOREVER:
        event = await bus.get()
        if event is STOP_ITERATION:
            hub.log.info("Event bus was forced to stop")
            return
        await hub.evbus.broker.propagate(contexts=contexts, event=event)


async def stop(hub):
    """
    Stop the event bus
    """
    if hub.evbus.BUS is not None:
        hub.log.debug("Stopping the event bus")
        await hub.evbus.BUS.put(STOP_ITERATION)

    hub.evbus.RUN_FOREVER = False


async def join(hub):
    while not hub.evbus.STARTED:
        await hub.pop.loop.sleep(0)
