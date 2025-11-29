import logging
from src.config import DEBUG_MODE

if not DEBUG_MODE:
    logging.getLogger('discord').setLevel(logging.CRITICAL)
    logging.getLogger('discord.http').setLevel(logging.CRITICAL)
    logging.getLogger('discord.client').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('asyncio').setLevel(logging.CRITICAL)
    
    logging.disable(logging.WARNING)
