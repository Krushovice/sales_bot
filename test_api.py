from app.api_v1.utils.request_api import OutlineHelper


outline_client = OutlineHelper()


key = outline_client.get_key(key_id=26)

outline_client.set_key_limit(key)


outline_client.remove_key_limit(key)
