# Checked the DecimalEncoder and Checks workarounds 20200402 and no progression towards fix

import boto3, json, os, decimal

SM_ARN = 'arn:aws:states:us-east-1:542671725628:stateMachine:PetCuddleOTron'

sm = boto3.client('stepfunctions')

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    # Print event data to logs  
    print("Received event: " + json.dumps(event))

    # Load data coming from APIGateway
    data = json.loads(event['body'])
 
    # Check that all parameters have come through from API gateway
    
    checks = []
    checks.append(data['buysell'] != "")
    checks.append(data['price'] != "")
    checks.append(data['car'] != "")
    checks.append( (data['email'] != "") or (data['phone'] != "") )
    

    # if any checks fail, return error to API Gateway
    if False in checks:
        response = {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin":"*"},
            "body": json.dumps( { "Status": "Error", "Reason": "Input failed validation" }, cls=DecimalEncoder )
        }
    # If none, start the state machine execution and inform client of 2XX success :)
    else: 
        #Call Lambda inside VPC which will communicate with RDS   
  
        responseFromVpc = lambda_client.invoke(
            FunctionName = 'arn:aws:lambda:us-east-1:542671725628:function:lambda-VPC-db-access',
            InvocationType = 'RequestResponse',
            Payload = json.dumps(data)
        )
 
        payloadFromVPC = json.load(responseFromVpc['Payload']) 
        vpcMessage = payloadFromVPC['VPC_message']   
        print(vpcMessage)
        
        #Sending the message coming from database to the user
        data['message'] = str(vpcMessage)
        
        #Telling the State machine whether to send sms, email, both or none
        if ((data['email'] != "") and (data['phone'] != "")):
            data['notification'] = "both"
        elif ((data['email'] != "") and (data['phone'] == "")):
            data['notification'] = "email"
        elif ((data['email'] == "") and (data['phone'] != "")) :
            data['notification'] = "sms"
        else: 
            data['notification'] = "none"
            
        print(data)
        
        sm.start_execution( stateMachineArn=SM_ARN, input=json.dumps(data, cls=DecimalEncoder) )
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            "body": json.dumps( {"Status": "Notification sent."}, cls=DecimalEncoder )
        }
    return response

# This is a workaround for: http://bugs.python.org/issue16535
# Solution discussed on this thread https://stackoverflow.com/questions/11942364/typeerror-integer-is-not-json-serializable-when-serializing-json-in-python
# https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

