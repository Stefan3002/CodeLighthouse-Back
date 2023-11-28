from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'secrieru2302@gmail.com'

new_announcement_message = MIMEMultipart("alternative")
new_announcement_message["Subject"] = "New Announcement in Lighthouse - CodeLighthouse"
# new_announcement_message["From"] = sender_email
# new_announcement_message["To"] = ''

# Create the plain-text and HTML version of your message
def format_new_announcement_email(username, lighthouse_name, announcement_content):
    html = f"""\
    <html>
      <body>
        <p>
        Hi, <b>{username}</b> <br />
        A new announcement has been made in the <b><i>{lighthouse_name}</i></b> Lighthouse!
        </p>
        <p>
        {announcement_content}
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    new_announcement_message.attach(part)