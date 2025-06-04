import redis
import json

r = redis.Redis(host='185.240.103.57', port='6379', decode_responses=True)


data = {"data":[{
                "id": 4,
                "title": "Category 4",
                "image": "string",
                "parent": {
                    "id": 3,
                    "title": "Category 3",
                    "image": "string",
                    "parent": {
                        "id": 2,
                        "title": "Category 2",
                        "image": "string",
                        "parent": {
                            "id": 1,
                            "title": "Category 1",
                            "image": "string"
                        }
                    }
                }
            }]
        }



# r.set('static-category', 'some-value')
# r.set('static-category', json.dumps(data), 60)
data = json.loads(r.get('static-category'))
print(data)