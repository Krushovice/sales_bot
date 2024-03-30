import unittest
from unittest.mock import AsyncMock, patch

from app.api_v1.utils.tools import send_logs_email

from app.api_v1.config import settings


class TestSendEmail(unittest.IsolatedAsyncioTestCase):

    @patch("app.api_v1.utils.tools.smtplib.SMTP")
    async def test_send_email(self, mock_smtp):
        # Создаем экземпляр smtplib.SMTP
        smtp_instance = mock_smtp.return_value

        # Проверяем отправку письма
        await send_logs_email()

        # Проверяем, что была вызвана установка TLS
        smtp_instance.starttls.assert_called_once()

        # Проверяем, что был выполнен вход в систему
        smtp_instance.login.assert_called_once_with(
            "Brezh69@yandex.ru", settings.EMAIL_PSWD
        )

        # Проверяем, что было отправлено сообщение
        smtp_instance.send_message.assert_called_once()


if __name__ == "__main__":
    unittest.main()
