import os

NUTRITIONIX_HEADERS = {
    'x-app-id': os.environ.get('x-app-id'),
    'x-app-key': os.environ.get('x-app-key'),
    'x-remote-user-id': '1'
}
REQUIRED_NATURAL_ARGUMENTS = ['food-description']
REQUIRED_MANUAL_ARGUMENTS = ['food-name', 'serving-unit', 'quantity', 'protein', 'carbohydrates', 'fat']
