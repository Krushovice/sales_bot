from outline_vpn.outline_vpn import OutlineVPN

from app.api_v1.config import settings


class OutlineHelper:
    def __init__(self):
        self.client = OutlineVPN(
            api_url=settings.OUTLINE_API_URL,
            cert_sha256=settings.OUTLINE_SHA_CERT,
        )

    async def create_new_key(self, name):
        key = self.client.create_key(name=str(name))
        return key

    async def get_key(self, key_id: int):
        key = self.client.get_key(key_id)
        if key:
            return key
        return None

    async def set_key_name(self, key, name):
        self.client.rename_key(key.key_id, str(name))

    async def delete_key(self, key_id: int):
        self.client.delete_key(key_id)

    async def set_key_limit(self, key_id: int):
        self.client.add_data_limit(key_id, 1000 * 1000 * 20)

    async def remove_key_limit(self, key_id: int):
        self.client.delete_data_limit(key_id)


outline_helper = OutlineHelper()
