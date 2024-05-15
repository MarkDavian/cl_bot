import json
from bson import ObjectId

class Storage:
    storage: dict


    def __init__(self) -> None:
        with open('storage/storage.json', 'r') as file:
            self.storage = json.load(file)

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        with open('storage/storage.json', 'w') as file: 
            json.dump(self.storage, file, indent=2, ensure_ascii=False)

    def get(self):
        return self.storage['all']
    
    def get_by_id(self, id: str):
        for c, item in enumerate(self.storage['all']):
            if item['id'] == id:
                return item

    def add(self, data: dict):
        id = data.get('id')
        if id is None:
            id = str(ObjectId())
            data['id'] = id
        self.storage['all'].append(data)
        return id
    
    def bulk_add(self, sequence: list[dict]):
        for data in sequence:
            self.add(data)

    def delete(self, id: str):
        for c, item in enumerate(self.storage['all']):
            if item['id'] == id:
                self.storage['all'].pop(c)