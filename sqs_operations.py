import json
import os
import boto3


QUEUE_URL=os.getenv('QUEUE_URL')


def get_queu_url(regionName: str, name_of_the_queue: str) -> dict:
    sqs_client = boto3.client('sqs', region_name=regionName)
    response = sqs_client.get_queue_url(QueueName=name_of_the_queue)
    print(response['QueueUrl'])
    return response['QueueUrl']


async def send_to_queue(domain_name: str):
    sqs_client = boto3.client('sqs', region_name="us-east-1")
    message = {"DomainName": domain_name}
    response = sqs_client.send_message(QueueUrl=QUEUE_URL,
                                       MessageBody=json.dumps(message))
    return response


async def receive_msg_from_queue():
    sqs_client = boto3.client('sqs', region_name="us-east-1")
    response = sqs_client.receive_message(QueueUrl=QUEUE_URL,
                                          MaxNumberOfMessages=1,
                                          WaitTimeSeconds=10)
    default_value = {"status": " key not found"}

    print(response.get("Messages", default_value))

    for msg in response["Messages"]:
        domain_name_from_queue = msg["Body"]
        DomainName = json.loads(domain_name_from_queue)

        recipt_handler = msg["ReceiptHandle"]
        delete_handled_messages(recipt_handler)

        return DomainName["DomainName"]


def delete_handled_messages(receipt_handler):
    sqs_client = boto3.client('sqs', region_name="us-east-1")
    response = sqs_client.delete_message(QueueUrl=QUEUE_URL,
                                         ReceiptHandle=receipt_handler)
    return "Deleted"


if __name__ == "__main__":
    region_name = "us-east-1"
    queue_name = "test_queue_1"

    get_queu_url(region_name, queue_name)


