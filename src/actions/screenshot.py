import io
import asyncio
from PIL import ImageGrab
from src.config import DEBUG_MODE


class ScreenshotAction:
    @staticmethod
    async def execute_command(context):
        try:
            screenshot_buffer = await ScreenshotAction._capture_screenshot()
            
            if screenshot_buffer is None:
                if isinstance(context, object) and hasattr(context, 'response'):
                    await context.response.send_message("Failed to capture screenshot", ephemeral=True)
                elif isinstance(context, object) and hasattr(context, 'send'):
                    await context.send("Failed to capture screenshot")
                return
            
            screenshot_buffer.seek(0)
            
            if isinstance(context, object) and hasattr(context, 'response'):
                file = __import__('discord').File(screenshot_buffer, filename="screenshot.png")
                await context.response.send_message(file=file, ephemeral=True)
            elif isinstance(context, object) and hasattr(context, 'send'):
                file = __import__('discord').File(screenshot_buffer, filename="screenshot.png")
                await context.send(file=file)
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error executing screenshot command: {e}")
    
    @staticmethod
    async def execute_channel_action(context=None):
        try:
            screenshot_buffer = await ScreenshotAction._capture_screenshot()
            
            if screenshot_buffer is None:
                if DEBUG_MODE:
                    print("Failed to capture screenshot for channel action")
                return
            
            screenshot_buffer.seek(0)
            await ScreenshotAction._upload_to_cdn(screenshot_buffer)
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error executing screenshot channel action: {e}")
    
    @staticmethod
    async def _capture_screenshot():
        try:
            loop = asyncio.get_event_loop()
            image = await loop.run_in_executor(None, ImageGrab.grab)
            
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            
            return buffer
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error capturing screenshot: {e}")
            return None
    
    @staticmethod
    async def _upload_to_cdn(screenshot_buffer):
        try:
            if DEBUG_MODE:
                print("Preparing to upload screenshot to CDN")
            
            pass
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"Error uploading screenshot to CDN: {e}")
