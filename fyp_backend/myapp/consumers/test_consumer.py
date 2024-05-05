import json
from channels.generic.websocket import AsyncWebsocketConsumer
from PIL import Image
import numpy as np
import io
import base64

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected'}))

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            # If text data is received
            await self.send(text_data=json.dumps({'message': 'Text data received'}))
            print("Text data received")
        elif bytes_data:
            # If binary data is received
            try:
                decoded_data = base64.b64decode(bytes_data)
                image = Image.open(io.BytesIO(decoded_data))
                resized_image = image.resize((224, 224))
                array = np.array(resized_image)
                if array.ndim == 2:
                    array = np.stack((array,) * 3, axis=-1)
                input_data = np.expand_dims(array, axis=0)
                # Process the image data here (e.g., using TensorFlow)
                # Then, send a response back to the client if needed
                await self.send(text_data=json.dumps({'message': 'Binary data received and processed'}))
                print("Binary data received")
            except Exception as e:
                print(f"Error processing image data: {e}")
                await self.send(text_data=json.dumps({'error': str(e)}))
        else:
            # If no data is received
            await self.send(text_data=json.dumps({'message': 'No data received'}))
            print("No data received")

    async def disconnect(self, close_code):
        print("WebSocket connection closed.")
