import imaplib
import email
import time
import re
import requests

IMAP_SERVER = 'imap.hostinger.com'
EMAIL_ACCOUNT = 'prueba@arcanejuanpa.shop'
EMAIL_PASSWORD = 'Losreyes12@@'
TELEGRAM_TOKEN = '7662157096:AAE5n-HqJPaREy3rJhB1uJUvR_DfwH6yAfI'
TELEGRAM_CHAT_ID = '1091978697'

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    requests.post(url, data=data)

def obtener_codigo_disney(cuerpo):
    # Buscar un código Disney (normalmente 6 números)
    match = re.search(r'\b(\d{6})\b', cuerpo)
    if match:
        return match.group(1)
    return None

def leer_correos():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select('inbox')

    status, mensajes = mail.search(None, 'UNSEEN')
    correos = mensajes[0].split()

    for correo_id in correos:
        status, datos = mail.fetch(correo_id, '(RFC822)')
        mensaje = email.message_from_bytes(datos[0][1])

        if mensaje.is_multipart():
            for parte in mensaje.walk():
                if parte.get_content_type() == 'text/plain':
                    cuerpo = parte.get_payload(decode=True).decode()
                    codigo = obtener_codigo_disney(cuerpo)
                    if codigo:
                        enviar_telegram(f"Código Disney+: {codigo}")
        else:
            cuerpo = mensaje.get_payload(decode=True).decode()
            codigo = obtener_codigo_disney(cuerpo)
            if codigo:
                enviar_telegram(f"Código Disney+: {codigo}")

    mail.logout()

if __name__ == "__main__":
    while True:
        leer_correos()
        time.sleep(15)
