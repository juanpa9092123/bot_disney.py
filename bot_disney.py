import imaplib
import email
import re
import requests
from bs4 import BeautifulSoup

# CONFIGURA AQUÍ TUS DATOS
IMAP_SERVER = 'imap.hostinger.com'
EMAIL_ACCOUNT = 'prueba@arcanejuanpa.shop'
EMAIL_PASSWORD = 'Losreyes12@@'
TELEGRAM_TOKEN = '7662157096:AAE5n-HqJPaREy3rJhB1uJUvR_DfwH6yAfI'
TELEGRAM_CHAT_ID = '1091978697'

# Función para limpiar HTML
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

# Función para enviar mensaje a Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text
    }
    requests.post(url, data=payload)

# Función para revisar correos
def check_email_for_code():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()

    # Lista de palabras que SÍ deben estar en el correo
    palabras_permitidas = ["iniciar sesión", "inicio de sesión", "código de ingreso", "acceder a Disney"]

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg["subject"]
                
                if subject:
                    subject = subject.lower()
                else:
                    subject = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if "attachment" not in content_disposition and content_type in ["text/plain", "text/html"]:
                            raw_text = part.get_payload(decode=True).decode()
                            text = clean_html(raw_text).lower()

                            # Revisamos si alguna palabra permitida está en el subject o en el cuerpo
                            if any(palabra in subject or palabra in text for palabra in palabras_permitidas):
                                match = re.search(r'(\d{6})', text)
                                if match:
                                    code = match.group(1)
                                    send_telegram_message(f"Código Disney+: {code}")
                                    print(f"Código Disney+: {code}")
                                else:
                                    print("No se encontró un código válido.")
                else:
                    raw_text = msg.get_payload(decode=True).decode()
                    text = clean_html(raw_text).lower()

                    if any(palabra in subject or palabra in text for palabra in palabras_permitidas):
                        match = re.search(r'(\d{6})', text)
                        if match:
                            code = match.group(1)
                            send_telegram_message(f"Código Disney+: {code}")
                            print(f"Código Disney+: {code}")
                        else:
                            print("No se encontró un código válido.")
    mail.logout()

# Ejecutar
check_email_for_code()
