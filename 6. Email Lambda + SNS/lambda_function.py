import boto3, os, json

FROM_EMAIL_ADDRESS = 'email@example.com'

ses = boto3.client('ses')

def lambda_handler(event, context):
    # Print event data to logs .. 
    print("Received event: " + json.dumps(event))
    # Publish message directly to email
    ses.send_email( Source=FROM_EMAIL_ADDRESS,
        Destination={ 'ToAddresses': [ event['Input']['email'] ] }, 
        Message={ 'Subject': {'Data': 'Here is what we found'},
            'Body': {'Text': {event['Input']['message']}}
        }
    )
    return 'Success!'
