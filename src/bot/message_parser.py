import re
from src.config import DEBUG_MODE


class MessageParser:
    @staticmethod
    def parse_mention_format(message_content):
        mention_pattern = r'<@!?(\d+)>'
        mentions = re.findall(mention_pattern, message_content)
        
        if not mentions:
            return None
        
        parts = message_content.split(None, 1)
        if len(parts) < 2:
            return None
        
        try:
            payload = parts[1]
            components = payload.split(':')
            if len(components) < 3:
                return None
            
            device_id = components[0].strip()
            device_name = components[1].strip()
            action = ':'.join(components[2:]).strip()
            
            return {
                'device_id': device_id,
                'device_name': device_name,
                'action': action
            }
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error parsing payload: {e}")
            return None
    
    @staticmethod
    def is_bot_mentioned(bot_id, message):
        if message.mentions:
            for mention in message.mentions:
                if mention.id == bot_id:
                    return True
        return False
