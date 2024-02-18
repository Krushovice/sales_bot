from outline_vpn.outline_vpn import OutlineVPN

from app.api_v1.config import settings


class OutlineHelper:
    # Setup the access with the API URL (Use the one provided to you after the server setup)
    def __init__(self):
        self.client = OutlineVPN(
            api_url=settings.OUTLINE_API_URL,
            cert_sha256=settings.OUTLINE_SHA_CERT,
        )

    def create_new_key(self, name):
        # Create a new key
        new_key = self.client.create_key(name=str(name))
        return new_key

    def get_key(self, key_id: int):
        return self.client.get_key(key_id)

    # Rename it
    def set_key_name(self, key, name):
        self.client.rename_key(key.key_id, str(name))

    # Delete it
    def delete_key(self, key):
        self.client.delete_key(key.key_id)

    # Set a monthly data limit for a key (20MB)
    def set_key_limit(self, key):
        self.client.add_data_limit(key.key_id, 1000 * 1000 * 20)

    # Remove the data limit
    def remove_key_limit(self, key):
        self.client.delete_data_limit(key.key_id)


outline_helper = OutlineHelper()
