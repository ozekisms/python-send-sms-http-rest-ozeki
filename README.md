### How to use the ozekilibsrest library

#### How to install the ozekilibsrest library

In order to install the __ozekilibsrest library__ you have to use the following command:

```python
pip install ozekilibsrest
```
After you have installed the library, you can import its contents into your project by using the following lines of code:

```python
from ozekilibsrest import Configuration, Message, MessageApi
```

#### Creating a Configuration

To send your SMS message to the built in API of the __Ozeki SMS Gateway__, your client application needs to know the details of your __Gateway__ and the __http_user__.
We can define a __Configuration__ instance with these lines of codes in Python.

```python
configuration = Configuration(
    username="http_user",
    password="qwe123",
    api_url="http://127.0.0.1:9509/api"
)
```

#### Creating a Message

After you have initialized your configuration object you can continue by creating a Message object.
A message object holds all the needed data for message what you would like to send.
In Python we create a __Message__ instance with the following lines of codes:

```python
msg = Message(
    to_address="+36201111111",
    text="Hello world!"
)
```

#### Creating a MessageApi

You can use the __MessageApi__ class of the __ozekilibsrest library__ to create a __MessageApi__ object which has the methods to send, delete, mark and receive SMS messages from the Ozeki SMS Gateway.
To create a __MessageApi__, you will need these lines of codes and a __Configuration__ instance.

```python
api = MessageApi(configuration)
```

After everything is ready you can begin with sending the previously created __Message__ object:

```python
result = api.send(msg)

print(result)
```

After you have done all the steps, you check the Ozeki SMS Gateway and you will see the message in the _Sent_ folder of the __http_user__.