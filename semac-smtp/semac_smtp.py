import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from gmail_smtp import create_service


class GmailSMTPServiceProvider:

    def __init__(self):
        self.client_secret_file = 'client_secret.json'
        self.api_name = 'gmail'
        self.api_version = 'v1'
        self.scopes = ['https://mail.google.com/']
        self.service = create_service(self.client_secret_file, self.api_name, self.api_version, self.scopes)

    def send_verification_code(self, to, code):
        random_code = code
        emailMsg = f'Parabéns! Você deu seus primeiros passos para iniciar sua aventura!\n\n' \
                   f'Seu código de verificação é: {random_code}\n\n' \
                   f'Vejo você pelos campos da justi... Espera, isso da processo...\n\nTe espero no evento!\n\n' \
                   f'Com <3 da comissão da SEMAC 2021'
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = to
        mimeMessage['subject'] = 'SEMAC 2021 - Código de verificação'
        mimeMessage.attach(MIMEText(emailMsg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        self.service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        return random_code


gmail_smtp_service_provider = GmailSMTPServiceProvider()

