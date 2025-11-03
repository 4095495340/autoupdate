import boto3
import os

LAYER_NAME = os.environ["LAYER_NAME"]
TARGET_FUNCTIONS = os.environ["TARGET_FUNCTIONS"].split(",")
AWS_REGION = os.environ.get("AWS_REGION") or boto3.session.Session().region_name
ACCOUNT_ID = os.environ["ACCOUNT_ID"]

lambda_client = boto3.client("lambda", region_name=AWS_REGION)

def get_latest_layer_version_arn():
    response = lambda_client.list_layer_versions(LayerName=LAYER_NAME)
    if not response["LayerVersions"]:
        raise Exception(f"No versions found for layer: {LAYER_NAME}")
    latest_version = response["LayerVersions"][0]
    return latest_version["LayerVersionArn"]

def update_lambda_function(function_name, new_layer_arn):
    config = lambda_client.get_function_configuration(FunctionName=function_name)
    existing_layers = config.get("Layers", [])
    existing_layer_arns = [l["Arn"] for l in existing_layers]

    if new_layer_arn in existing_layer_arns:
        print(f"{function_name} already has the latest layer version.")
        return

    # Replace old versions of this layer
    updated_layers = [arn for arn in existing_layer_arns if not arn.startswith(f"arn:aws:lambda:{AWS_REGION}:{ACCOUNT_ID}:layer:{LAYER_NAME}")]
    updated_layers.append(new_layer_arn)

    lambda_client.update_function_configuration(
        FunctionName=function_name,
        Layers=updated_layers
    )
    print(f"Updated {function_name} with layer version {new_layer_arn}")

def lambda_handler(event, context):
    print("Triggered by event:", event)
    new_layer_arn = get_latest_layer_version_arn()
    for fn in TARGET_FUNCTIONS:
        update_lambda_function(fn.strip(), new_layer_arn)