import os
import io
import qrcode
import smtplib
from PIL import Image
import email.message
from dotenv import load_dotenv

load_dotenv()


def qr_generator(content):
    data = content
    img = qrcode.make(data)
    return img


def image_to_bytes(image: Image):
    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    bytes_array = buffer.getvalue()
    return bytes_array


def send_email(email_receiver: str, id_badge: int):
    body_email = """
        <h1> Você criou uma nova medalha </h1>
 
        <p>Disponibilize o QRCode abaixo da forma que achar melhor.

        """

    msg = email.message.EmailMessage()
    msg['Subject'] = "Nova Medalha - GamIF"
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = email_receiver
    password = os.getenv("EMAIL_ID_PASSWORD")
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body_email)

    img = qr_generator(id_badge)

    someobject_bytes = image_to_bytes(img)

    msg.add_attachment(someobject_bytes, maintype='image', subtype='jpg', filename='qrcode.jpg')

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()

    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
