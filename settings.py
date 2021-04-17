import os

NUTRITIONIX_HEADERS = {
    'x-app-id': os.environ.get('x-app-id', '110d0c06'),
    'x-app-key': os.environ.get('x-app-key', '02457cbe48e42b5050da9898c21ccc06'),
    'x-remote-user-id': '1'
}
REQUIRED_NATURAL_ARGUMENTS = ['food-description']
REQUIRED_MANUAL_ARGUMENTS = ['food-name', 'serving-unit', 'quantity', 'protein', 'carbohydrates', 'fat']
