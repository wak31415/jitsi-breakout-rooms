# By William Koch

import sys
import time
import math
import string
import random
import getpass
import smtplib, ssl
from email.mime.text import MIMEText

email_config = {}

# CONFIGURE YOUR EMAIL ACCOUNT BELOW THIS LINE

email_config["your_name"]                   = "John Doe"

email_config["your_email"]                  = "your_email_address"

# e.g. "Your Jitsi Breakout Room"
email_config["subject"]                     = "[interesting subject line]"

# Give your event a meaningful name. It will be part of the link.
# Can be left empty
email_config["event_name"]                  = ""

# what file are the email addresses stored in?
email_config["email_addr_file_location"]    = "email_addresses.txt"

# how big do you want the teams to be?
email_config["team_size"]                   = 4

# Your outgoing mail server, e.g. "smtp.web.de"
email_config["smtp_server"]                 = "your_smtp_server"

# The following normally does not have to be modified. Check with your email provider
# server port
email_config["port"]                        = 587

## DO NOT MODIFY BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING


def send_email(TO, password, link):
    """
    TO: list of email addresses\n
    password: email password\n
    link: jitsi meet link\n
    """
    with open("message.txt","r") as f:
        message = f.read()

    if message.find("{link}")<0:
        message = message + f"\n\n{link}"

    message = message.replace("{link}", link)
    message = message.replace("{name}", email_config["your_name"])

    context = ssl.create_default_context()

    msg = MIMEText(message)
    msg['Subject'] = email_config["subject"]
    msg['From'] = email_config["your_email"]
    msg['To'] = email_config["your_email"]
    msg['BCC'] = ", ".join(TO)


    with smtplib.SMTP(email_config["smtp_server"], email_config["port"]) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(email_config["your_email"], password)
        server.send_message(msg)
        server.close()


def load_addr_from_file(path):
    """
    path: file path containing email addresses. Each email address should be on a
    seperate line
    """
    addr_list = []
    try:
        with open(path,"r") as f:
            for addr in f:
                addr = addr.strip()
                addr_list.append(addr)
    except:
        print(f"File '{path}' not found")
        sys.exit(0)

    if len(addr_list) == 0:
        print("ERROR: no email addresses found")
    return addr_list


def generate_link():
    event_name = email_config["event_name"].lower()
    event_name = event_name.replace(" ", "-") + "-"
    prefix = f"https://meet.jit.si/{event_name}"
    numbers = ''.join([random.choice(string.digits) for _ in range(10)])
    return prefix + numbers


if __name__ == "__main__":
    if email_config["your_email"] == "your_email_address":
        print("Which email account are you sending this from?")
        email_config["your_email"] = input("Email address: ")

    if email_config["smtp_server"] == "your_smtp_server":
        print("What is your outgoing mailserver (smtp)?")
        email_config["smtp_server"] = input("SMTP server: ").strip()
    
    print("Enter your account password below:")
    try:
        p = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
    else:
        if len(p)==0: 
            print("You entered an empty password...")

    addr_list = load_addr_from_file(email_config["email_addr_file_location"])

    random.shuffle(addr_list)

    team_size = email_config["team_size"]
    num_teams = math.ceil(len(addr_list)/team_size)
    teams = [[] for _ in range(num_teams)]

    for _ in range(team_size):
        for i in range(num_teams):
            if not addr_list: break
            teams[i].append(addr_list.pop())

    for team in teams:
        link = generate_link()
    
        send_email(team, p, link)
        print('Emails sent to', team)
        time.sleep(1)
