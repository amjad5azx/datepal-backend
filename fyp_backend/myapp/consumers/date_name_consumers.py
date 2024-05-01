import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pymongo import MongoClient

class DateNameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket connection closed.")

    async def receive(self, text_data=None, bytes_data=None):
        try:
            print("Received text data:", text_data)
            if text_data.startswith("date_name:"):
                date_name = text_data.split(":")[1].strip()
                uri = "mongodb+srv://amjad5azx:amjad1290@cluster0.imlsmty.mongodb.net/"
                client = MongoClient(uri)
                db = client["DateDB"]
                collection_names = db.list_collection_names()

                collection = db[collection_names[0]]
                record = collection.find_one({"name": date_name}, {"_id": 0})

                if record:
                    await self.send(text_data=json.dumps(record))
                else:
                    await self.send(text_data=json.dumps({'error': f"No record found for date '{date_name}'."}))
            else:
                await self.send(text_data=json.dumps({'error': "Invalid request format. Please provide the date name."}))
        except Exception as e:
            print(f"Error processing date request: {e}")
            await self.send(text_data=json.dumps({'error': str(e)}))
