from ozekilibsrest import Configuration, MessageApi

configuration = Configuration(
    username="http_user",
    password="qwe123",
    api_url="http://127.0.0.1:9509/api"
)

api = MessageApi(configuration)

results = api.download_incoming()

print(results)

for result in results.messages:
    print(result)
