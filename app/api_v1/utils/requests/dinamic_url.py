from outline_vpn.outline_vpn import OutlineKey

from app.api_v1.config import settings


def gen_outline_dynamic_link(key: OutlineKey) -> str:
    user_id = int(key.name)
    # Формируем динамический ключ из данных о ключе
    dynamic_link = (
        f"{settings.OUTLINE_USERS_GATEWAY}/conf/{key.password}{hex(user_id)}#RealVPN"
    )

    return dynamic_link
