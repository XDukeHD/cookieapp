from src.config import DEBUG_MODE


class ActionLoader:
    _actions = {}
    
    @staticmethod
    def load_actions():
        try:
            from src.actions.screenshot import ScreenshotAction
            ActionLoader._actions['screenshot'] = ScreenshotAction
            
            if DEBUG_MODE:
                print(f"Loaded {len(ActionLoader._actions)} action(s)")
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error loading actions: {e}")
    
    @staticmethod
    def get_action(action_name):
        return ActionLoader._actions.get(action_name)
    
    @staticmethod
    def get_available_actions():
        return list(ActionLoader._actions.keys())
    
    @staticmethod
    async def execute_action(action_name, context, trigger_type='command'):
        try:
            from src.bot.authentication import AuthenticationManager
            
            auth = AuthenticationManager()
            
            if trigger_type == 'channel':
                if not auth.is_authenticated():
                    if DEBUG_MODE:
                        print(f"Channel action '{action_name}' ignored: client not authenticated")
                    return False
            
            action_class = ActionLoader.get_action(action_name)
            
            if not action_class:
                if DEBUG_MODE:
                    print(f"Action '{action_name}' not found")
                return False
            
            if trigger_type == 'command':
                await action_class.execute_command(context)
            elif trigger_type == 'channel':
                await action_class.execute_channel_action(context)
            
            return True
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error executing action '{action_name}': {e}")
            return False
