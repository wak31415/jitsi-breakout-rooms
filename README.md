# jitsi-breakout-rooms
## Breakout rooms for Jitsi Meet

Given a list of email addresses of all participants, randomly assign them to a group and send every member of the group a link to a Jitsi Meet video call via email. Currently only available as a CLI tool, GUI application coming up!

Simply download the `send_emails.py` file and configure the settings in the head of the file (i.e. which email account you are sending the emails from, your outgoing mail server, the size of the breakout rooms, etc.).

## Running the program
By default, the Python script sends the message in the file `message.txt`. An example message is included. 

**Important:** Include the tags `{link}` in the messag - this is where the actual link will be placed. If the tag is not found in the message text, the link will simply be appended to the end of the email message.
The tag `{name}` is also available but doesn't need to be specified. This is your name. 

Make sure you have a recent version of Python installed, you will need at least Python 3. Then you can simply run 

```bash
python send_emails.py
```

You will be prompted to enter your account password. Don't worry if it doesn't look like it's taking any input, this is normal and is to protect your input from spying eyes.

## Email address list
The email addresses should be in a simple text file containing only the email addresses, and each address should be on a separate line. It doesn't matter if the file is a `.csv` or `.txt` (any file extension is fine, as long as it is a basic text file). Remember to modify the filepath in the configuration section in `send_emails.py`.

## Note on 2FA
This will probably not work with email accounts that are protected by two factor authentication. I would therefore recommend you to create/use a spam account for this purpose.