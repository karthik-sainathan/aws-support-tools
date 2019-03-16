# Copyright 2018-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

import json
import boto3

client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    #print (event)
    if (event['triggerSource'] == 'UserMigration_Authentication'):
        # authenticate the user as an Admin
        user = client.admin_initiate_auth(
            UserPoolId='<user pool id of the user pool where the user already exists>',
            ClientId='<app client id of the user pool where the user already exists>',
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': event['userName'],
                'PASSWORD': event['request']['password']
            }
        )
        #print (user)
        if (user):
            userAttributes = client.get_user(
                AccessToken=user['AuthenticationResult']['AccessToken']
            )
            for userAttribute in userAttributes['UserAttributes']:
                if userAttribute['Name'] == 'email':
                    userEmail = userAttribute['Value']
                    #print(userEmail)
                    # Set the email attribute to be returned in the event response to Cognito
                    event['response']['userAttributes'] = {
                        "email": userEmail,
                        "email_verified": "true"
                    }
            event['response']['finalUserStatus'] = "CONFIRMED"
            event['response']['messageAction'] = "SUPPRESS"
            print (event)
            return (event)
        else:
            return('Bad Password')
    elif (event["triggerSource"] == "UserMigration_ForgotPassword"):
        # Get the user details as an Admin
        user = client.admin_get_user(
            UserPoolId='<user pool id of the user pool where the already user exists>',
            Username=event['userName']
        )
        if (user):
            for userAttribute in user['UserAttributes']:
                if userAttribute['Name'] == 'email':
                    userEmail = userAttribute['Value']
                    print(userEmail)
                    # Set the email attribute to be returned in the event response to Cognito
                    event['response']['userAttributes'] = {
                        "email": userEmail,
                        "email_verified": "true"
                    }
            event['response']['messageAction'] = "SUPPRESS"
            
            print (event)
            return (event)
        else:
            return('Bad Password')
            
    else:
        return('there was an error')