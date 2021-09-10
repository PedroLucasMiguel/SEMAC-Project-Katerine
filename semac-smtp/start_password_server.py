import time
import os
import datetime
from semac_smtp import gmail_smtp_service_provider

if __name__ == '__main__':
    last_valid_line = ''
    next_line = 0
    today = datetime.datetime.today()

    os.rename('password-emails-queue.txt', f'Logs/{today.timestamp()}-password-emails-queue.txt')

    with open('password-emails-queue.txt', 'w') as new_file:
        new_file.close()

    with open('password-emails-queue.txt', 'r') as queue:
        while True:
            line = queue.readline()

            if last_valid_line != line:
                if line == '':
                    queue.seek(last_valid_line)
                    print('No new email in the file')
                else:
                    print(line)
                    last_line = line
                    email_and_code = line.split(' ')
                    email_and_code[1] = email_and_code[1].replace('\n', '')
                    gmail_smtp_service_provider.send_forgot_password_code(email_and_code[0], email_and_code[1])
                    print(f'\nSended email to: {email_and_code[0]} | Code: {email_and_code[1]}')
                    last_valid_line = queue.tell()
                    time.sleep(1)

            time.sleep(2)
