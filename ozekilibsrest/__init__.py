__author__ = "Zsolt Ardai"
__email__ = "info@ozeki.hu"


from uuid import uuid4, UUID
from datetime import datetime, timedelta
from json import dumps, loads
from base64 import b64encode
from enum import Enum
from requests import post, get


class Configuration:
    def __init__(self, username=None, password=None, api_url=None):
        if username is not None:
            self.username = username
        else:
            self.username = ''
        if password is not None:
            self.password = password
        else:
            self.password = ''
        if api_url is not None:
            self.api_url = api_url
        else:
            self.api_url = ''


class Message:
    def __init__(self, message_id=None, from_connection=None, from_address=None,
                 from_station=None,  to_connection=None, to_address=None,
                 to_station=None, text=None, create_date=None, valid_until=None,
                 time_to_send=None, is_submit_report_requested=None,
                 is_delivery_report_requested=None, is_view_report_requested=None):
        if message_id is not None and (isinstance(message_id, str) or isinstance(message_id, UUID)):
            self.message_id = message_id
        else:
            self.message_id = uuid4()
        if from_connection is not None and isinstance(from_connection, str):
            self.from_connection = from_connection
        else:
            self.from_connection = ''
        if from_address is not None and isinstance(from_address, str):
            self.from_address = from_address
        else:
            self.from_address = ''
        if from_station is not None and isinstance(from_station, str):
            self.from_station = from_station
        else:
            self.from_station = ''
        if to_connection is not None and isinstance(to_connection, str):
            self.to_connection = to_connection
        else:
            self.to_connection = ''
        if to_address is not None and isinstance(to_address, str):
            self.to_address = to_address
        else:
            self.to_address = ''
        if to_station is not None and isinstance(to_station, str):
            self.to_station = to_station
        else:
            self.to_station = ''
        if text is not None and isinstance(text, str):
            self.text = text
        else:
            self.text = ''
        if create_date is not None and isinstance(create_date, datetime):
            self.create_date = create_date
        else:
            self.create_date = datetime.now()
        if valid_until is not None and isinstance(valid_until, datetime):
            self.valid_until = valid_until
        else:
            self.valid_until = datetime.now() + timedelta(days=7)
        if time_to_send is not None and isinstance(time_to_send, datetime):
            self.time_to_send = time_to_send
        else:
            self.time_to_send = datetime.now()
        if is_submit_report_requested is not None and isinstance(is_submit_report_requested, bool):
            self.is_submit_report_requested = is_submit_report_requested
        else:
            self.is_submit_report_requested = True
        if is_delivery_report_requested is not None and isinstance(is_delivery_report_requested, bool):
            self.is_delivery_report_requested = is_delivery_report_requested
        else:
            self.is_delivery_report_requested = True
        if is_view_report_requested is not None and isinstance(is_view_report_requested, bool):
            self.is_view_report_requested = is_view_report_requested
        else:
            self.is_view_report_requested = True
        self.tags = []

    def add_tag(self, name, value):
        if isinstance(name, str) and isinstance(value, str):
            self.tags.append({"name": name, "value": value})

    def __str__(self):
        return f"{ self.from_address }->{ self.to_address } '{ self.text }'"

    def to_json(self):
        json_object = {}
        if self.message_id != '':
            json_object["message_id"] = str(self.message_id)
        if self.from_connection != '':
            json_object["from_connection"] = self.from_connection
        if self.from_address != '':
            json_object["from_address"] = self.from_address
        if self.from_station != '':
            json_object["from_station"] = self.from_station
        if self.to_connection != '':
            json_object["to_connection"] = self.to_connection
        if self.to_address != '':
            json_object["to_address"] = self.to_address
        if self.to_station != '':
            json_object["to_station"] = self.to_station
        if self.text != '':
            json_object["text"] = self.text
        json_object["create_date"] = self.create_date.strftime("%Y-%m-%dT%H:%M:%S")
        json_object["valid_until"] = self.valid_until.strftime("%Y-%m-%dT%H:%M:%S")
        json_object["time_to_send"] = self.time_to_send.strftime("%Y-%m-%dT%H:%M:%S")
        json_object["submit_report_requested"] = self.is_submit_report_requested
        json_object["delivery_report_requested"] = self.is_delivery_report_requested
        json_object["view_report_requested"] = self.is_view_report_requested
        json_object["tags"] = self.tags

        return json_object


class MessageApi:
    def __init__(self, configuration):
        if isinstance(configuration, Configuration):
            self._configuration = configuration
        else:
            self._configuration = Configuration()

    @staticmethod
    def create_authorization_header(username, password):
        username_password = f'{ username }:{ password }'
        return f'Basic { b64encode(username_password.encode()).decode() }'

    @staticmethod
    def create_request_body(messages=None):
        if messages is None:
            messages = []
        elif isinstance(messages, Message):
            messages = [messages]

        json_object = {}
        json_array = []

        for message in messages:
            json_array.append(message.to_json())

        json_object["messages"] = json_array

        return dumps(json_object)

    @staticmethod
    def create_request_body_to_manipulate(folder=None, messages=None):
        if messages is None:
            messages = []
        elif isinstance(messages, Message):
            messages = [messages]

        if folder is None:
            folder = "inbox"
        elif isinstance(folder, Folder):
            if folder == Folder.Inbox:
                folder = "inbox"
            if folder == Folder.Outbox:
                folder = "outbox"
            if folder == Folder.Sent:
                folder = "sent"
            if folder == Folder.NotSent:
                folder = "notsent"
            if folder == Folder.Deleted:
                folder = "deleted"

        json_object = {}
        json_array = []

        for message in messages:
            json_array.append(message.message_id)

        json_object["folder"] = folder
        json_object["message_ids"] = json_array

        return dumps(json_object)

    def send(self, message=None):
        authorization_header = self.create_authorization_header(self._configuration.username,
                                                                self._configuration.password)
        request_body = self.create_request_body(messages=message)
        results = self.get_response_send(self.do_request_post(self.create_uri_to_send_sms(self._configuration.api_url),
                                                              authorization_header,
                                                              request_body))
        if results.total_count == 1:
            return results.results[0]
        else:
            return results

    def delete(self, folder=None, message=None):
        authorization_header = self.create_authorization_header(self._configuration.username,
                                                                self._configuration.password)
        request_body = self.create_request_body_to_manipulate(folder=folder, messages=message)
        result = self.get_response_manipulate(self.do_request_post(self.create_uri_to_delete_sms(self._configuration.api_url),
                                                                   authorization_header, request_body), "delete", message)
        if result.total_count == 1:
            if result.success_count == 1:
                return True
            else:
                return False
        else:
            return result

    def mark(self, folder=None, message=None):
        authorization_header = self.create_authorization_header(self._configuration.username,
                                                                self._configuration.password)
        request_body = self.create_request_body_to_manipulate(folder=folder, messages=message)
        result = self.get_response_manipulate(self.do_request_post(self.create_uri_to_mark_sms(self._configuration.api_url),
                                                                   authorization_header, request_body), "mark", message)
        if result.total_count == 1:
            if result.success_count == 1:
                return True
            else:
                return False
        else:
            return result

    def download_incoming(self):
        authorization_header = self.create_authorization_header(self._configuration.username,
                                                                self._configuration.password)
        result = self.get_response_receive(self.do_request_get(self.create_uri_to_receive_sms(self._configuration.api_url,
                                                                                              Folder.Inbox),
                                                               authorization_header))
        self.delete(folder=Folder.Inbox, message=result.messages)
        return result


    @staticmethod
    def do_request_post(url, authorization_header, request_body):
        headers = {"Authorization": authorization_header, "Content-Type": "application/json"}
        response = post(url, data=request_body, headers=headers)
        return loads(response.text)

    @staticmethod
    def do_request_get(url, authorization_header):
        headers = {"Authorization": authorization_header}
        response = get(url, headers=headers)
        return loads(response.text)

    @staticmethod
    def create_uri_to_send_sms(url=None):
        if url is not None and isinstance(url, str):
            base_url = url.split('?')[0]
            return f'{ base_url }?action=sendmsg'
        else:
            return ''

    @staticmethod
    def create_uri_to_delete_sms(url=None):
        if url is not None and isinstance(url, str):
            base_url = url.split('?')[0]
            return f'{ base_url }?action=deletemsg'
        else:
            return ''

    @staticmethod
    def create_uri_to_mark_sms(url=None):
        if url is not None and isinstance(url, str):
            base_url = url.split('?')[0]
            return f'{ base_url }?action=markmsg'
        else:
            return ''

    @staticmethod
    def create_uri_to_receive_sms(url=None, folder=None):
        if url is not None and isinstance(url, str) and isinstance(folder, Folder):
            base_url = url.split('?')[0]
            if folder == Folder.Inbox:
                folder = "inbox"
            if folder == Folder.Outbox:
                folder = "outbox"
            if folder == Folder.Sent:
                folder = "sent"
            if folder == Folder.NotSent:
                folder = "notsent"
            if folder == Folder.Deleted:
                folder = "deleted"
            return f'{ base_url }?action=receivemsg&folder={ folder }'
        else:
            return ''

    @staticmethod
    def get_response_send(response=None):
        if response is not None and response.get('http_code') == 200:
            data = response.get('data')
            results = MessageSendResults(data.get('total_count'), data.get('success_count'), data.get('failed_count'))
            for object in data.get('messages'):
                message = Message()
                if 'message_id' in object:
                    message.message_id = object.get('message_id')
                if 'from_connection' in object:
                    message.from_connection = object.get('from_connection')
                if 'from_address' in object:
                    message.from_address = object.get('from_address')
                if 'from_station' in object:
                    message.from_station = object.get('from_station')
                if 'to_connection' in object:
                    message.to_connection = object.get('to_connection')
                if 'to_address' in object:
                    message.to_address = object.get('to_address')
                if 'to_station' in object:
                    message.to_station = object.get('to_station')
                if 'text' in object:
                    message.text = object.get('text')
                if 'create_date' in object:
                    message.create_date = datetime.strptime(object.get('create_date'), "%Y-%m-%d %H:%M:%S")
                if 'valid_until' in object:
                    message.valid_until = datetime.strptime(object.get('valid_until'), "%Y-%m-%d %H:%M:%S")
                if 'time_to_send' in object:
                    message.time_to_send = datetime.strptime(object.get('time_to_send'), "%Y-%m-%d %H:%M:%S")
                if 'submit_report_requested' in object:
                    message.is_submit_report_requested = object.get('submit_report_requested')
                if 'delivery_report_requested' in object:
                    message.is_delivery_report_requested = object.get('delivery_report_requested')
                if 'view_report_requested' in object:
                    message.is_view_report_requested = object.get('view_report_requested')
                if 'tags' in object and len(object.get('tags')) > 0:
                    tags = object.get('tags')
                    for tag in tags:
                        message.add_tag(tag.get('name'), tag.get('value'))
                if 'status' in object:
                    if object.get('status') == 'SUCCESS':
                        status = DeliveryStatus.Success
                        response_message = ''
                    else:
                        status = DeliveryStatus.Failed
                        response_message = object.get('status')
                else:
                    status = DeliveryStatus.Failed
                    response_message = ''

                result = MessageSendResult(message, status, response_message)
                results.add_result(result)
            return results
        else:
            return MessageSendResults()

    @staticmethod
    def get_response_manipulate(response=None, method=None, messages=None):
        if not isinstance(messages, list):
            messages = [messages]
        if response is not None and response.get('http_code') == 200:
            if method == "delete":
                data = response.get('data')
                result = MessageDeleteResult(data.get('folder'))
                for message in messages:
                    success = False
                    for message_id in data.get('message_ids'):
                        if message_id == str(message.message_id):
                            success = True
                    if success:
                        result.add_id_remove_succeeded(str(message.message_id))
                    else:
                        result.add_id_remove_failed(str(message.message_id))
                return result
            else:
                data = response.get('data')
                result = MessageMarkResult(data.get('folder'))
                for message in messages:
                    success = False
                    for message_id in data.get('message_ids'):
                        if message_id == str(message.message_id):
                            success = True
                    if success:
                        result.add_id_mark_succeeded(str(message.message_id))
                    else:
                        result.add_id_mark_failed(str(message.message_id))
                return result
        else:
            if method == 'delete':
                return MessageDeleteResult()
            else:
                return MessageMarkResult()

    @staticmethod
    def get_response_receive(response=None):
        if response is not None and response.get('http_code') == 200:
            data = response.get('data')
            result = MessageReceiveResult(response.get('folder'), response.get('limit'))
            for object in data.get('data'):
                message = Message()
                if 'message_id' in object:
                    message.message_id = object.get('message_id')
                if 'from_connection' in object:
                    message.from_connection = object.get('from_connection')
                if 'from_address' in object:
                    message.from_address = object.get('from_address')
                if 'from_station' in object:
                    message.from_station = object.get('from_station')
                if 'to_connection' in object:
                    message.to_connection = object.get('to_connection')
                if 'to_address' in object:
                    message.to_address = object.get('to_address')
                if 'to_station' in object:
                    message.to_station = object.get('to_station')
                if 'text' in object:
                    message.text = object.get('text')
                if 'create_date' in object:
                    message.create_date = datetime.strptime(object.get('create_date'), "%Y-%m-%d %H:%M:%S")
                if 'valid_until' in object:
                    message.valid_until = datetime.strptime(object.get('valid_until'), "%Y-%m-%d %H:%M:%S")
                if 'time_to_send' in object:
                    message.time_to_send = datetime.strptime(object.get('time_to_send'), "%Y-%m-%d %H:%M:%S")
                if 'submit_report_requested' in object:
                    message.is_submit_report_requested = object.get('submit_report_requested')
                if 'delivery_report_requested' in object:
                    message.is_delivery_report_requested = object.get('delivery_report_requested')
                if 'view_report_requested' in object:
                    message.is_view_report_requested = object.get('view_report_requested')
                if 'tags' in object and len(object.get('tags')) > 0:
                    tags = object.get('tags')
                    for tag in tags:
                        message.add_tag(tag.get('name'), tag.get('value'))
                result.add_message(message)
            return result
        else:
            return MessageReceiveResult()

class Folder(Enum):
    Inbox = "inbox"
    Outbox = "outbox"
    Sent = "sent"
    NotSent = "notsent"
    Deleted = "deleted"


class DeliveryStatus(Enum):
    Success = "Success"
    Failed = "Failed"


class MessageSendResult:
    def __init__(self, message=None, status=None, response_message=None):
        if message is not None:
            self.message = message
        else:
            self.message = Message()
        if status is not None and isinstance(status, DeliveryStatus):
            if status == DeliveryStatus.Success:
                self.status = 'Success'
            else:
                self.status = 'Failed'
        else:
            self.status = DeliveryStatus.Failed
        if response_message is not None and isinstance(response_message, str):
            self.response_message = response_message
        else:
            self.response_message = ''

    def __str__(self):
        return f'{ self.status }, { self.message }'


class MessageSendResults:
    def __init__(self, total_count=None, success_count=None, failed_count=None):
        if total_count is not None:
            self.total_count = total_count
        else:
            self.total_count = 0
        if success_count is not None:
            self.success_count = success_count
        else:
            self.success_count = 0
        if failed_count is not None:
            self.failed_count = failed_count
        else:
            self.failed_count = 0

        self.results = []

    def add_result(self, result=None):
        if result is not None and isinstance(result, MessageSendResult):
            self.results.append(result)

    def __str__(self):
        return f'Total: { self.total_count }. Success: { self.success_count }. Failed: { self.failed_count }.'


class MessageDeleteResult:
    def __init__(self, folder=None):
        if folder is not None:
            if folder == "inbox":
                self.folder = Folder.Inbox
            elif folder == "outbox":
                self.folder = Folder.Outbox
            elif folder == "sent":
                self.folder = Folder.Sent
            elif folder == "notsent":
                self.folder = Folder.NotSent
            else:
                self.folder = Folder.Deleted
        else:
            self.folder = Folder.Inbox
        self.message_ids_remove_succeeded = []
        self.message_ids_remove_failed = []
        self.total_count = 0
        self.success_count = 0
        self.failed_count = 0

    def add_id_remove_succeeded(self, message_id=None):
        if message_id is not None and isinstance(message_id, str):
            self.message_ids_remove_succeeded.append(message_id)
            self.total_count += 1
            self.success_count += 1

    def add_id_remove_failed(self, message_id=None):
        if message_id is not None and isinstance(message_id, str):
            self.message_ids_remove_failed.append(message_id)
            self.total_count += 1
            self.failed_count += 1

    def __str__(self):
        return f'Total: { self.total_count }. Success: { self.success_count }. Failed: { self.failed_count }.'


class MessageMarkResult:
    def __init__(self, folder=None):
        if folder is not None:
            if folder == "inbox":
                self.folder = Folder.Inbox
            elif folder == "outbox":
                self.folder = Folder.Outbox
            elif folder == "sent":
                self.folder = Folder.Sent
            elif folder == "notsent":
                self.folder = Folder.NotSent
            else:
                self.folder = Folder.Deleted
        else:
            self.folder = Folder.Inbox
        self.message_ids_mark_succeeded = []
        self.message_ids_mark_failed = []
        self.total_count = 0
        self.success_count = 0
        self.failed_count = 0

    def add_id_mark_succeeded(self, message_id=None):
        if message_id is not None and isinstance(message_id, str):
            self.message_ids_mark_succeeded.append(message_id)
            self.total_count += 1
            self.success_count += 1

    def add_id_mark_failed(self, message_id=None):
        if message_id is not None and isinstance(message_id, str):
            self.message_ids_mark_failed.append(message_id)
            self.total_count += 1
            self.failed_count += 1

    def __str__(self):
        return f'Total: { self.total_count }. Success: { self.success_count }. Failed: { self.failed_count }.'


class MessageReceiveResult:
    def __init__(self, folder=None, limit=None):
        if folder is not None:
            if folder == "inbox":
                self.folder = Folder.Inbox
            elif folder == "outbox":
                self.folder = Folder.Outbox
            elif folder == "sent":
                self.folder = Folder.Sent
            elif folder == "notsent":
                self.folder = Folder.NotSent
            else:
                self.folder = Folder.Deleted
        else:
            self.folder = Folder.Inbox
        if limit is not None and isinstance(limit, str):
            self.limit = limit
        else:
            self.limit = '1000'
        self.messages = []

    def add_message(self, message=None):
        if message is not None and isinstance(message, Message):
            self.messages.append(message)

    def __str__(self):
        return f'Message count: { len(self.messages) }.'