# Raspberry Pi Tracker

This is a serverless deployment for tracking Raspberry Pi 4 model B 4GB for India Region.

This app is deployed using Netlify for UI and S3+API Gateway+Lambda as backend and DynamoDB as Database.

There are 2 Lambda Functions.

1. Is responsible for scraping URL's and updating DynamoDB data every 15 minutes (using eventbrigde)
2. Is responsible for getting data from DynamoDB and is executed through API call from API Gateway.

## Prerequisites

1. Terraform
2. AWS Account
3. Netlify Account (_optional_)

## Installation steps

Backend Deploy -

1. Clone repo
2. Run `terraform init`
3. Do a dry run `terraform plan`
4. Apply changes `terraform apply`, enter `yes` when prompted

Frontend Deploy -

For frontend any service can be used. I have setup this branch with Netlify to watch the files in `UI` directory.
