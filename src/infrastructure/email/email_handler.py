from typing import List
from pydantic import EmailStr, BaseModel
from jinja2 import Environment, select_autoescape, PackageLoader
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from src.infrastructure.config.app_config import get_settings

env = Environment(
    loader=PackageLoader('src', 'infrastructure/email/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Email:
    def __init__(self, user: dict, url: str, email: List[EmailStr]):
        self.name = user['username']
        self.sender = 'AlkohoLove <info@serwer2254722.home.pl>'
        self.email = email
        self.url = url
        pass

    async def send_mail(self, subject, template):
        settings = get_settings()
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_USERNAME,
            MAIL_PASSWORD=settings.EMAIL_PASSWORD,
            MAIL_FROM=EmailStr(settings.EMAIL_FROM),
            MAIL_PORT=settings.EMAIL_PORT,
            MAIL_SERVER=settings.EMAIL_HOST,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')

        html = template.render(
            url=self.url,
            first_name=self.name,
            subject=subject
        )

        # Define the message options
        message = MessageSchema(
            subject=subject,
            recipients=self.email,
            body=html,
            subtype="html"
        )

        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)

    async def send_verification_code(self):
        await self.send_mail('AlkohoLove email verification', 'verification')

    async def send_reset_password_code(self):
        await self.send_mail('AlkohoLove password reset request', 'reset_password')

    async def send_delete_account_code(self):
        await self.send_mail('AlkohoLove account deletion request', 'delete_account')
