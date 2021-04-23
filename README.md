# Buy/Sell Car App

* This app allows you to buy or sell a car.
* If you choose to buy, the app will search the database for cars matching your criteria and send you an email and sms with the amount of cars it found.
* If you choose to sell, it will add an entry to the database with the details of your car.

## Table of Contents

1. [Tech Stack](#tech-stack)
1. [Mockup](#mockup)
1. [AWS Diagram](#aws-diagram)
1. [Frontend App](#frontend-app)
1. [API Gateway](#api-gateway)
1. [Lambdas](#lambdas)
1. [Step Functions](#step-functions)
1. [SNS/SES](#sns-ses)

## Tech Stack

1. HTML/CSS/Javascript
1. AWS API Gateway
1. AWS Lambda
1. AWS RDS MySQL
1. AWS Step Functions
1. AWS SNS/SES

## Mockup

![alt text](https://github.com/mviisan/buysellcarservice/blob/master/app_mockup.png?raw=true)

## AWS Diagram

![alt text](https://github.com/mviisan/buysellcarservice/blob/master/diagram.png?raw=true) 

## Frontend App
Website allows user to buy or sell car.

## API Gateway
API Gateway exposes an API endpoint. API Gateway then communicates with main lambda. 

## Lambdas
Main lambda receives information from the API Gateway and first communicates with lambda inside VPC (which will communicate with the RDS instance). Main lambda then calls Step Functions.

## Step Functions
Step Functions orchestrate additional lambda (to access SNS) and SES

## SNS SES
SNS and SES send emails and sms