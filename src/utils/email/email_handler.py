from os import getenv
from typing import List

from fastapi import Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from jinja2 import Environment, select_autoescape, PackageLoader

from src.infrastructure.config.app_config import ApplicationSettings, get_settings

env = Environment(
    loader=PackageLoader('src', 'utils/email/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Email:
    def __init__(self, user: dict, url: str, email: List[EmailStr]):
        self.name = user['username']
        self.sender = 'AlkohoLove <admin@admin.com>'
        self.email = email
        self.url = url
        pass

    async def send_mail(self, subject, template, settings: ApplicationSettings = Depends(get_settings)):
        # Define the config
        # TODO use variables
        conf = ConnectionConfig(
            MAIL_USERNAME='47e96bff33bbac',
            MAIL_PASSWORD='a42af6529c988f',
            MAIL_FROM=EmailStr('admin@admin.com'),
            MAIL_PORT=2525,
            MAIL_SERVER='smtp.mailtrap.io',
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
        await self.send_mail('Your verification code (Valid for 10min)', 'verification')
