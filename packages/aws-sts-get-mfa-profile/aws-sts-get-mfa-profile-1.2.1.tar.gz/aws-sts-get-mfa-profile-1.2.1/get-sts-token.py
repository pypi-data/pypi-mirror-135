import boto3
from botocore.exceptions import ClientError
import sys
import os
import pytz
from pathlib import Path
boto3.setup_default_session(profile_name='mfa')
credential_file_path = str(Path.home())+'\\.aws\\credentials'

AWS_ACCESS_KEY_ID = os.popen('aws configure get aws_access_key_id --profile mfa').read().strip()
print(f'AWS Access Key ID: [{"*"*(len(AWS_ACCESS_KEY_ID)-4)+AWS_ACCESS_KEY_ID[-4:]}]')

AWS_SECRET_ACCESS_KEY = os.popen('aws configure get aws_secret_access_key --profile mfa').read().strip()
print(f'AWS Secret Access Key: [{"*"*(len(AWS_SECRET_ACCESS_KEY)-4)+AWS_SECRET_ACCESS_KEY[-4:]}]')

AWS_MFA_SERIAL = os.popen('aws configure get mfa_serial --profile mfa').read().strip()

try:
    SESSION_DURATION = int(input("How many seconds do you want the token to last for? [Default = 86400]: ") or 86400)
except ValueError:
    print('Please retry using only integers in seconds.')
    sys.exit(1)

ONE_TIME_PASSWORD = input("Please enter your 6 digit one time password: ")

if len(str(ONE_TIME_PASSWORD)) != 6:
    print('Invalid one time password.')
    sys.exit(1)

sts_client = boto3.client('sts')

token_response = sts_client.get_session_token(
    DurationSeconds=SESSION_DURATION,
    SerialNumber=AWS_MFA_SERIAL,
    TokenCode=str(ONE_TIME_PASSWORD)
)

token_credentials = token_response['Credentials']
expiry = token_credentials['Expiration'].astimezone(pytz.timezone('Australia/Adelaide'))
print('\nToken will expire at', expiry)

os.system(f'aws configure set aws_access_key_id {token_credentials["AccessKeyId"]} --profile default')
print(f'New AWS Access Key ID: {token_credentials["AccessKeyId"]}')

os.system(f'aws configure set aws_secret_access_key {token_credentials["SecretAccessKey"]} --profile default')
print(f'New AWS Secret Access Key: {token_credentials["SecretAccessKey"]}')

os.system(f'aws configure set aws_session_token {token_credentials["SessionToken"]} --profile default')
print(f'New AWS Session Token: {token_credentials["SessionToken"]}')