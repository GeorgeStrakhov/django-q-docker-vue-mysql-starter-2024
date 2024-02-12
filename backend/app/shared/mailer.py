import os
from django.conf import settings
from postmarker.core import PostmarkClient
from postmarker.models.emails import EmailManager
from app.logging import logger
from string import Template

POSTMARK_API_TOKEN = os.getenv('POSTMARK_API_TOKEN')

if not POSTMARK_API_TOKEN:
    raise Exception('POSTMARK_API_TOKEN is not set')

mail_client = PostmarkClient(server_token=POSTMARK_API_TOKEN)

base_email_template = Template('''

<!DOCTYPE html>
<html>
<head>
    <title>$title</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }
        .container { background-color: #f8f8f8; padding: 20px; }
        .logo { margin-bottom: 20px; }
        .button { background-color: #87f6fa; padding: 10px 20px; margin-top: 20px; text-decoration: none; border-radius: 5px; border: 1px solid #000;}
        .footer { margin-top: 20px; font-size: 0.8em; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        $content
    </div>
</body>
</html>

''')
