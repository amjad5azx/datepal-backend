from channels.generic.websocket import AsyncWebsocketConsumer
from PIL import Image
import numpy as np
import io
import json
import tensorflow as tf
import base64
from pymongo import MongoClient
import tensorflow as tf


class_names = ['Ajwa', 'Galaxy', 'Jujube', 'Nabtat Ali', 'Rutab', 'Sabzo', 'Shaishe', 'Sokari', 'Sugaey']


class DateImageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected'}))

    async def receive(self, text_data=None, bytes_data=None):
        try:
            decoded_data = base64.b64decode(text_data.split(",")[1])  # Extract base64 data part
            image = Image.open(io.BytesIO(decoded_data))
            resized_image = image.resize((224, 224))
            array = np.array(resized_image)
            if array.ndim == 2:
                array = np.stack((array,) * 3, axis=-1)
            input_data = np.expand_dims(array, axis=0)
            model = tf.keras.models.load_model('model.h5')
            # model = tf.keras.layers.TFSMLayer("my_model_300_Epoch", call_endpoint='serving_default')
            predictions = model.predict(input_data)
            predicted_class_index = np.argmax(predictions)
            predicted_class_name = class_names[predicted_class_index]

            uri = "mongodb+srv://amjad5azx:amjad1290@cluster0.imlsmty.mongodb.net/"

            client = MongoClient(uri)
            if client is not None:
                print("Connected to MongoDB Atlas successfully.")
            else:
                print("Failed to connect to MongoDB Atlas.")

            db = client["DateDB"]

            collection_names = db.list_collection_names()
            print("Available collections:", collection_names)
                
            collection=db[collection_names[0]]
            record = collection.find_one({"name": predicted_class_name}, {"_id": 0})
            # record = {"name": predicted_class_name}

                
            if record:
                await self.send(text_data=json.dumps(record))
            else:
                await self.send(text_data=json.dumps({'prediction': predicted_class_name, 'record': None}))
        except Exception as e:
            print(f"Error processing image data: {e}")
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def disconnect(self, close_code):
        print("WebSocket connection closed.")