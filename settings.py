import os
from itsdangerous import URLSafeTimedSerializer
from app_config import MAIL_USERNAME, SECRET_KEY

NUTRITIONIX_HEADERS = {
    'x-app-id': os.environ.get('x-app-id'),
    'x-app-key': os.environ.get('x-app-key'),
    'x-remote-user-id': '1'
}
EMAIL = MAIL_USERNAME
serializer = URLSafeTimedSerializer(SECRET_KEY)
TOKEN_AGE = 259200
