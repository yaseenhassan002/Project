from .BaseDataModel import BaseDataModel
from .dB_shemes import data_chunk
from .enums.DataBaseenum import DataBaseenum
from bson.objectid import ObjectId
from pymongo import InsertOne 
from .dB_shemes.data_chunk import Datachunk 


class cchunkDatamodel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseenum.COLLECTION_PROJECT_NAME.value]


    @classmethod

    async def create_instances(cls, db_client: object):
        instances = cls(db_client)
        await instances.init_collection()
        return instances

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseenum.COLLECTION_CHUNK_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseenum.COLLECTION_CHUNK_NAME.value]
            indexes = Datachunk.get_index()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name = index['name'],
                    unique = index["unique"]
                    
                )




    async def create_chunk(self, Chunk: data_chunk):
        result = await self.collection.insert_one(Chunk.dict(by_alias = True, exclude_unset = True))
        Chunk._id = result.inserted_one
        return Chunk
    

    async def get_chunk(self, chunk_id: str):
        result = self.collection.find_one({
            "_id": ObjectId(chunk_id)
        })

        if result is None:
            return None

        return data_chunk(**result)


    async def insert_many_chunk(self, Chunks: list, batch_size: int = 100):
        
        for i in range(0, len(Chunks), batch_size):
            batch = Chunks[i: i+batch_size]

            operations = [
                InsertOne(Chunk.dict(by_alias = True, exclude_unset = True))
                for Chunk in batch
            ]

            await self.collection.bulk_write(operations)

            return len (Chunks)
    
    async def delete_chunks_by_project_id_(self, project_id: ObjectId):
        result = self.collection.delete_many({
            "chunk_project_id": project_id
        })
