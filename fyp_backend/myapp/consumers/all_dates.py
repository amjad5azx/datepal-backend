import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pymongo import MongoClient

class AllDatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        try:
            # Connect to MongoDB
            uri = "mongodb+srv://amjad5azx:amjad1290@cluster0.imlsmty.mongodb.net/"
            client = MongoClient(uri)
            db = client["DateDB"]
            collection_names = db.list_collection_names()

            # Fetch all records from MongoDB
            all_records = {}
            for collection_name in collection_names:
                collection = db[collection_name]
                records = list(collection.find({}, {"_id": 0}))  # Convert cursor to list
                all_records[collection_name] = records

            # Send all records over WebSocket
            await self.send(text_data=json.dumps(all_records))

        except Exception as e:
            print(f"Error processing date request: {e}")
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def disconnect(self, close_code):
        print("WebSocket connection closed.")

    async def receive(self, text_data=None, bytes_data=None):
        pass
