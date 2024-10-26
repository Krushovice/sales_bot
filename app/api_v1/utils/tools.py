import datetime
import os

from aiogram.types import Message


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP

from app.api_v1.orm import User, AsyncOrm, Key

from app.api_v1.config import settings

from .payment import set_expiration_date
from .requests import outline_helper


async def count_active_referrals(tg_id: int) -> int:
    refs = await AsyncOrm.get_active_referrals(tg_id=tg_id)
    return len(refs)


async def get_subscribe_info(user: User) -> dict:
    info = {}

    sub_date = user.expiration_date

    if user.subscription:
        info["subscribe"] = f"Активна до {sub_date}"

    else:
        info["subscribe"] = "Не активна"

    discount = await count_active_referrals(user.tg_id)

    if discount and discount > 0:
        info["discount"] = discount

    else:
        info["discount"] = 0

    return info


async def check_for_referral(message: Message):
    if len(message.text) > 6:
        target = str(message.text)[6:]
        referral_id = int(target)
        user = await AsyncOrm.get_user(tg_id=referral_id)
        if user:
            return referral_id
        else:
            return False
    return False


async def handle_referrer_user(referrer: User, duration: int) -> None:

    exp_date = referrer.expiration_date

    referrer_user_expiration = set_expiration_date(
            duration=duration,
            rest=exp_date,
            is_referrer=True,
        )
    if referrer.discount == 5:
        await AsyncOrm.update_user(
            tg_id=referrer.tg_id,
            expiration_date=referrer_user_expiration,
            )
    else:
        await AsyncOrm.update_user(
            tg_id=referrer.tg_id,
            discount=5,
            expiration_date=referrer_user_expiration,
            )


async def work_with_user_key(
        tg_id: int,
        expiration: str,
        user: User,
        payment_id: int,
) -> str:
    today = datetime.datetime.today().date()
    if not user.key:
        key = outline_helper.create_new_key(name=tg_id)

        await AsyncOrm.update_user(
            tg_id=tg_id,
            subscription=True,
            subscribe_date=today.strftime("%d-%m-%Y"),
            expiration_date=expiration,
            key=Key(
                api_id=int(key.key_id),
                name=key.name,
                user_id=user.id,
                value=key.access_url,
            ),
            payment=int(payment_id),
        )

        msg = ("Подписка успешно оплачена, ваш ключ\n"
               f"<pre>{key.access_url}</pre>\n"
               "Cкопируйте его ✅\n")
    else:
        await AsyncOrm.update_user(
            tg_id=tg_id,
            subscription=True,
            subscribe_date=today.strftime("%d-%m-%Y"),
            expiration_date=expiration,
            payment=int(payment_id),
        )

        outline_helper.remove_key_limit(key_id=user.key.api_id)
        msg = "Подписка оплачена, доступ не ограничен 🛜"

    return msg


async def send_logs_email():
    # Параметры почтового сервера
    smtp_host = "smtp.yandex.ru"
    smtp_port = 587
    smtp_user = settings.EMAIL
    smtp_password = settings.EMAIL_PSWD

    # Получение текущей даты и времени
    today = datetime.datetime.today().strftime("%d-%m-%Y")

    # Путь к папке с логами
    logs_folder = os.path.abspath("logs")

    # Формирование списка файлов в папке с логами
    log_files = [
        f
        for f in os.listdir(logs_folder)
        if os.path.isfile(os.path.join(logs_folder, f))
    ]

    # Формирование текста письма с прикрепленными лог-файлами
    message = MIMEMultipart()
    message["From"] = smtp_user
    message["To"] = settings.EMAIL
    message["Subject"] = f"Логи за {today}"

    body = "В папке с логами находятся следующие файлы:\n\n"
    for log_file in log_files:
        body += f"- {log_file}\n"

    message.attach(MIMEText(body, "plain"))

    for log_file in log_files:
        # Чтение содержимого файла
        with open(os.path.join(logs_folder, log_file), "r") as file:
            attachment = MIMEText(file.read(), "plain")
            attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=log_file,
            )
            message.attach(attachment)

    # Отправка письма
    async with SMTP(
        hostname=smtp_host,
        port=smtp_port,
        username=smtp_user,
        password=smtp_password,
    ) as smtp:
        await smtp.send_message(message)
