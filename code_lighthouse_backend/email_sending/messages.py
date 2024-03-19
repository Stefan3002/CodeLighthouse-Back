from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'secrieru2302@gmail.com'


new_grade_message = MIMEMultipart("alternative")
new_grade_message["Subject"] = "New Grade - CodeLighthouse"

def format_new_grade_email(username, lighthouse_name, grade, assignment_title, content):
    html = f"""\
    <html>
      <body>
        <p>
        Hi, <b>{username}</b> <br />
        You have received a new grade: <b><i>{grade}</i></b>.<br />
        Details: <br /> {assignment_title} in {lighthouse_name}.
        </p>
        <p>
        {content}
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    new_grade_message.attach(part)


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

new_account_message = MIMEMultipart("alternative")
new_account_message["Subject"] = "You have been registered for a contest - CodeLighthouse"
def format_new_account_email(username, password, announcement_content):
    html = f"""\
    <html>
      <body>
        <p>
        Hi, <b>{username}</b> <br />
        You have been <b>registered</b> for a contest! <br />
        </p>
        <p>
        Username / e-mail: {username} <br/>
        Password: {password} <br/>
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
    new_account_message.attach(part)




new_admin_message = MIMEMultipart("alternative")
new_admin_message["Subject"] = "Status update on your Challenge - CodeLighthouse"
# new_announcement_message["From"] = sender_email
# new_announcement_message["To"] = ''

# Create the plain-text and HTML version of your message
def format_new_admin_email(username, challenge_name, announcement_content):
    html = f"""\
    <html>
      <body>
        <p>
        Hi, <b>{username}</b> <br />
        An admin has reviewed your challenge  <b><i>{challenge_name}</i></b>!
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
    new_admin_message.attach(part)