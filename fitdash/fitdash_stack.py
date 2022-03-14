from cgitb import handler
from crypt import methods
from pickle import GET
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class FitdashStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fitdash_table = dynamodb.Table(self, "fitdash",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING), table_name= "fitdash"
        )

        get_totals_lambda = lambda_.Function(self, "get-totals-lambda", 
        runtime= lambda_.Runtime.PYTHON_3_9,
        code = lambda_.Code.from_asset('resources/get_totals'),
        handler = 'get_totals.handler',
        environment = {'TABLE_NAME': str(fitdash_table.table_name)})

        post_results_lambda = lambda_.Function(self, "post-results-lambda", 
        runtime= lambda_.Runtime.PYTHON_3_9,
        code = lambda_.Code.from_asset('resources/post_results'),
        handler = 'post_results.handler',
        environment = {'TABLE_NAME': str(fitdash_table.table_name)})

        get_totals_api = apigateway.LambdaRestApi(self,"get-totals-api",
        handler = get_totals_lambda)

        post_results_api = apigateway.LambdaRestApi(self,"post-results-api", 
        handler = post_results_lambda)

        fitdash_table.grant_read_write_data(get_totals_lambda)
        fitdash_table.grant_read_write_data(post_results_lambda)