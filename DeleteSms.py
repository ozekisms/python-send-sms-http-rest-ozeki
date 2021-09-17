from ozekilibsrest import Configuration, Message, MessageApi, Folder

configuration = Configuration(
    username="http_user",
    password="qwe123",
    api_url="http://127.0.0.1:9509/api"
)

msg = Message(
    message_id="e2259da4-e806-4ce2-b02b-e47905772625"
)

api = MessageApi(configuration)

result = api.delete(Folder.NotSent, msg)

print(result)