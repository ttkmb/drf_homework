from urllib.parse import urlparse

from django.core.validators import URLValidator
from rest_framework import serializers


def LinkValidator(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except serializers.ValidationError:
        raise serializers.ValidationError('Invalid URL')

    parsed_url = urlparse(value)
    if parsed_url.netloc != 'www.youtube.com':
        raise serializers.ValidationError('The URL is not from YouTube')
