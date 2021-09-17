from ozekilibsrest import Configuration, Message, MessageApi

configuration = Configuration(
    username="http_user",
    password="qwe123",
    api_url="http://127.0.0.1:9509/api"
)

msg = Message(
    to_address="+3620111111",
    text="Hello world!"
)

api = MessageApi(configuration)

result = api.send(msg)

print(result)
