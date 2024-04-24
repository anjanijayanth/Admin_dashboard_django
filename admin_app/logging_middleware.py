import datetime
import json
import pymongo
from . import settings

def connect_to_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["dashboard_logs_db"]
    collection = db["logs"]
    return collection
    
class UserLoggingMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        collection = connect_to_mongodb()
        user = request.user        
        try:
            if request.content_type == "application/json":
                request_body = json.loads(request.body.decode())
            elif request.content_type.startswith("application/x-www-form-urlencoded"):
                request_body = request.POST
            else:
                request_body = request.body.decode(errors='replace')
            request_modified = request_body[:100] if isinstance(request_body, str) else request_body
        except (UnicodeDecodeError, AttributeError, json.JSONDecodeError) as e:
            request_modified = f"Error processing request body: {e}"
        
        try:
             if request_modified['password']:
                 request_modified['password'] = "*******"
        except:
             pass
        log_data = {
            'user': user.username if user.is_authenticated else 'Anonymous',
            'url': request.build_absolute_uri(),
            'timestamp': datetime.datetime.now(),
            'method': request.method,
            'remote_addr': request.META.get('REMOTE_ADDR'),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'request_body':request_modified
        }
        response = self.get_response(request)
        log_data["response_status_code"]= response.status_code
        collection.insert_one(log_data)

        return response