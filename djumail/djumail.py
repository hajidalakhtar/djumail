from __future__ import print_function
from pyfiglet import figlet_format
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import click
import pickle
import os.path
from inscriptis import get_text
import os
from base64 import urlsafe_b64encode
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tqdm import tqdm
from simple_term_menu import TerminalMenu
import sys
import time
import subprocess
from termcolor import cprint
from colorama import init
init(strip=not sys.stdout.isatty())

# GMAIL SCRIPT
SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.addons.current.action.compose']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_873440156379-hrjs46tfnnbkgbi4o5d49tfn8ff60p3q.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('gmail', 'v1', credentials=creds)


def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def get_mail_body(msg_id, count, label):
    msg = service.users().messages().get(
        userId='me', id=msg_id, format="full").execute()
    try:
        payload = msg['payload']
        headers = payload['headers']
        parts = payload.get('parts')[0]
        data = parts['body']['data']
        data = data.replace("-", "+").replace("_", "/")
        decoded_data = base64.b64decode(data)
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
        print("\033[93mSubject : \033[0m", subject)
        print("\033[93mFrom : \033[0m", sender)
        soup = BeautifulSoup(decoded_data, "lxml")
        body = soup.get_text()
        print("\033[93mBody : \033[0m"+body)
        terminal_menu = TerminalMenu(
            ["Back"], title="Action")
        choice_index = terminal_menu.show()
        if(choice_index == 0):
            get_email_again(count, label)
    except:
        payload = msg['payload']
        headers = payload['headers']
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
            if d['name'] == 'From':
                sender = d['value']
        print("\033[93mSubject : \033[0m", subject)
        print("\033[93mFrom : \033[0m", sender)
        print("\033[93mBody : \033[0m"+"Cannot Get Body Email\n")

        terminal_menu = TerminalMenu(
            ["Back"], title="Action")
        choice_index = terminal_menu.show()
        if(choice_index == 0):
            get_email_again(count, label)


def get_email_again(count, label):
    os.system('cls||clear')
    cprint(figlet_format('DJUMAIL', font='big'), attrs=['bold'])

    global messages_subject
    global messages_id

    terminal_menu = TerminalMenu(messages_subject, title="Select Mail")
    choice_index = terminal_menu.show()

    get_mail_body(messages_id[choice_index], count, label)


# Send Email
def send():
    os.system('cls||clear')
    cprint(figlet_format('DJUMAIL', font='big'), attrs=['bold'])

    to = input("\033[93mTo :\033[0m ")
    subject = input("\033[93mSubject :\033[0m ")
    message_text = input("\033[93mMaessage :\033[0m ")

    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = to
    mimeMessage['from'] = "me"
    mimeMessage['subject'] = subject
    mimeMessage.attach(MIMEText(message_text, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes())
    raw_string = raw_string.decode()
    message = service.users().messages().send(
        userId="me", body={"raw": raw_string}).execute()
    select_label = TerminalMenu(["Send Again", "Back"], title="Action")
    choice_label = select_label.show()
    if choice_label == 0:
        send()
    else:
        main()


@ click.command()
@ click.option('--count', default=10, help='Masukan Jumlah Email Yang ingin anda ambil')
@ click.option('--label', default="IMPORTANT", help='Masukan Label email yang ingin anda ambil')
def receive(count, label):
    label_data = service.users().labels().list(userId="me").execute()
    labels = label_data.get('labels', [])
    option_label = []

    for label in labels:
        option_label.append(label["id"])

    select_label = TerminalMenu(option_label, title="Select Label")
    choice_label = select_label.show()

    # print(option_label)
    global messages_subject
    global messages_id
    os.system('cls||clear')
    cprint(figlet_format('DJUMAIL', font='big'), attrs=['bold'])

    results = service.users().messages().list(
        userId='me', labelIds=option_label[choice_label]).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No Email found.')
    else:
        results = service.users().messages().list(
            userId='me', labelIds=option_label[choice_label]).execute()
        messages = results.get('messages', [])
        messages_subject = []
        messages_id = []
        if len(messages) >= count:
            count = input("Count Mail? : ")
            print('Get Mail')

            for i in tqdm(range(int(count))):
                msg = service.users().messages().get(
                    userId='me', id=messages[i]['id']).execute()
                headers = msg["payload"]["headers"]
                body = msg["payload"]["body"]
                subject = [i['value']
                           for i in headers if i["name"] == "Subject"]
                messages_subject.append(smart_truncate(subject[0]))
                messages_id.append(messages[i]['id'])
        else:
            for i in tqdm(range(len(messages))):
                msg = service.users().messages().get(
                    userId='me', id=messages[i]['id']).execute()
                headers = msg["payload"]["headers"]
                body = msg["payload"]["body"]
                subject = [i['value']
                           for i in headers if i["name"] == "Subject"]
                messages_subject.append(smart_truncate(subject[0]))
                messages_id.append(messages[i]['id'])
        # messages_subject.append('\033[93m< Back\033[0m')
        os.system('cls||clear')
        cprint(figlet_format('DJUMAIL', font='big'), attrs=['bold'])
        terminal_menu = TerminalMenu(messages_subject, title="Select Mail")
        choice_index = terminal_menu.show()
        get_mail_body(messages_id[choice_index], count, label)
        # questions = [
        #     inquirer.List('gmail',
        #                   message="What size do you need?",
        #                   choices=gmail,

        #                   ),
        #     # inquirer.Text('name', message="What's your name"),
        # ]
        # answers = inquirer.prompt(questions)
        # print(answers)


def main():
    os.system('cls||clear')
    cprint(figlet_format('DJUMAIL', font='big'), attrs=['bold'])
    terminal_menu = TerminalMenu(["receive", "send"], title="Select Action")
    choice_index = terminal_menu.show()
    if choice_index == 0:
        receive()
    else:
        send()


if __name__ == '__main__':
    main()
