#!/usr/bin/env python3

import argparse
import logging
import sys
import uuid
from time import sleep

import boto3
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser()
parser.add_argument("--queue-name", "-q", default="Messages", help="SQS queue name")
parser.add_argument("--interval", "-i", default=0.1, help="timer interval", type=float)
parser.add_argument("--message", "-m", help="message to send")
parser.add_argument("--log", "-l", default="INFO", help="logging level")
args = parser.parse_args()

if args.log:
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=args.log)
else:
    parser.print_help(sys.stderr)

sqs = boto3.client("sqs")

try:
    logging.info(f"Getting queue URL for queue: {args.queue_name}")
    response = sqs.get_queue_url(QueueName=args.queue_name)
except ClientError as e:
    logging.error(e)
    exit(1)

queue_url = response["QueueUrl"]

logging.info(f"Queue URL: {queue_url}")

while True:
    try:
        message = str(uuid.uuid4())
        logging.info("Sending message: " + message)
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        logging.info("MessageId: " + response["MessageId"])
        sleep(args.interval)
    except ClientError as e:
        logging.error(e)
        exit(1)
