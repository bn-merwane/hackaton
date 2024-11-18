import os

environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
    print(f"Using {environment} settings")

elif environment == 'development':
    from .development import *
    print(f"Using {environment} settings")

else:
    raise ValueError(f"Invalid DJANGO_ENV: {environment}. Must be 'development' or 'production'.")