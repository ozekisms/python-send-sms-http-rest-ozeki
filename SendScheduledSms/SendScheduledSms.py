from ozekilibsrest import Configuration, Message, MessageApi
from datetime import datetime

configuration = Configuration(
    username="http_user",
    password="qwe123",
    api_url="http://127.0.0.1:9509/api"
)

msg = Message(
    to_address="+3620111111",
    text="Hello world!",
    time_to_send=datetime.strptime("2021-09-10 14:25:00", "%Y-%m-%d %H:%M:%S")
)

api = MessageApi(configuration)

result = api.send(msg)

print(result)