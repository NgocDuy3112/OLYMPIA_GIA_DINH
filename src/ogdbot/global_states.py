import asyncio

voice_client = None
reset_event = asyncio.Event()
messages = {}