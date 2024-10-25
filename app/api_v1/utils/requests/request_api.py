import secrets
from outline_vpn.outline_vpn import OutlineVPN

from app.api_v1.config import settings


class OutlineHelper:
    def __init__(self, api_url: str, cert_sha256: str):
        self.client = OutlineVPN(
            api_url=api_url,
            cert_sha256=cert_sha256,
        )

    def create_new_key(self, name):
        key = self.client.create_key(
            name=str(name),
            method="chacha20-ietf-poly1305",
            password=secrets.token_hex(6),
        )
        return key

    def get_key(self, key_id: int):
        key = self.client.get_key(key_id)
        if key:
            return key
        return None

    def get_keys(self):
        keys = self.client.get_keys()
        return keys

    def set_key_name(self, key, name):
        self.client.rename_key(key.key_id, str(name))

    def delete_key(self, key_id: int):
        self.client.delete_key(key_id)

    def set_key_limit(self, key_id: int):
        self.client.add_data_limit(key_id, 1000 * 1000 * 20)

    def remove_key_limit(self, key_id: int):
        self.client.delete_data_limit(key_id)


outline_helper = OutlineHelper(
    api_url=settings.NEW_OUTLINE_API_URL,
    cert_sha256=settings.NEW_OUTLINE_CERT,
)
