import json


class WorkerService:
    def __init__(self, client, queue_url):
        self.queue_url = queue_url
        self.worker_service = client

    def create_queue_chanel(self, queue_name):
        self.worker_service.create_queue(QueueName=queue_name)

    def send_message_into_queue(self, message_body, queue_chanel):
        self.worker_service.send_message(
            QueueUrl=self.generate_queue_url(queue_chanel),
            DelaySeconds=1,
            MessageBody=(json.dumps({
                **message_body,
            })))

    def receive_message(self, queue_name):
        response = self.worker_service.receive_message(
            QueueUrl=self.generate_queue_url(queue_name),
            MaxNumberOfMessages=1,
            MessageAttributeNames=['All'],
            VisibilityTimeout=0,
            WaitTimeSeconds=0)

        if "Messages" in response:
            message = response['Messages']
            self.delete_message_from_queue(message[0]['ReceiptHandle'],
                                           queue_name)
            return response['Messages'][0]['Body']

    def delete_message_from_queue(self, receipt_handle, queue_name):
        self.worker_service.delete_message(
            QueueUrl=self.generate_queue_url(queue_name),
            ReceiptHandle=receipt_handle)

    def generate_queue_url(self, queue_name):
        return self.queue_url + '/queue/' + queue_name

    def check_does_queue_exist(self, queue_name):
        response = self.worker_service.list_queues()
        if self.generate_queue_url(queue_name) not in response['QueueUrls']:
            self.create_queue_chanel(queue_name)
