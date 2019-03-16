# How to use migration trigger with Cognito User Pools

## Issue

I want a way to migrate the users from one User Pool to another without having the users sign up again. How do I accomplish this?

## Short Description

A typical use case that this issue arises from is when you want to modify the required attributes of a User Pool after it's creation. In this scenario, you would have to create a new User Pool with the desired attributes followed by migrating the users from the previous User Pool to the new User Pool.

## Resolution

Making use of a User migration Lambda trigger allows migration of the users from the existing User Pool to the new User Pool without having the users sign up again. You can also make use of this Lambda trigger to migrate users from any user directory apart from User Pool.

The points to consider for a Cognito User Migration lambda function are as follows:

1) You will have to use the USER_PASSWORD_AUTH flow in order to pass user's existing username and password to the Lambda function which you can then use to authenticate the user from the existing user directory, in this case - an existing User Pool. 

2) A logic needs to be provided to change the default Auth flow to USER_PASSWORD_AUTH when a user does not exist in the new User Pool (and does exist in the existing User Pool). For example the cognito-identity-js SDK uses SRP Auth by default, you will have to make sure that the Auth flow switches to USER_PASSWORD_AUTH when a user existing in the existing User Pool and not existing in the new User Pool tries to log into the new User Pool. Upon this login attempt, the Auth flow should be changed to SRP Auth for all future login attempts. 