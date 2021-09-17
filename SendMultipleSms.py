from ozekilibsrest import Configuration, Message, MessageApi

configuration = Configuration(
    username="http_user",
    password="qwe123",
    api_url="http://127.0.0.1:9509/api"
)

msg1 = Message(
    to_address="+3620111111",
    text="Hello world 1!"
)

msg2 = Message(
    to_address="+36202222222",
    text="Hello world 2!"
)

msg3 = Message(
    to_address="+36203333333",
    text="Hello world 3!"
)

api = MessageApi(configuration)

result = api.send([msg1, msg2, msg3])

print(result)