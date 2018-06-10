
# Taken Amazonlinux image as base on top of that installed required dependencies like make,awscli,python3.6,pip,and numpy

sudo docker build -t my_aws_image .

#create a docker container 

sudo docker run -it --net=host --name=my_aws_container -v           /Users/user_name/my_project/src/lambda_package:/zipped_lambda_package my_aws_image /bin/bash

# zipped all source code with dependency to be deployed to aws lambda

cd /my_project/src

zip /zipped_lambda_package/package.zip lambda_function.py

cd /my_project/src/lambda_package/

zip -ur /zipped_lamda_package/package.zip *

# lambda_function_create target defined in makefile to deploy zip package to AWS Lambda using aswcli

make lambda_function_create