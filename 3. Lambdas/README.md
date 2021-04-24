Main lambda calls VPC lambda, which connects to the RDS instance.

To deploy the lambda-vpc-db-access lambda and include dependencies in the package:
https://docs.aws.amazon.com/lambda/latest/dg/python-package-create.html#python-package-create-with-dependency

IAM roles are required for lambda to call other lambda and other VPC components (in this case, RDS instance). These are stored in the iam_roles directory