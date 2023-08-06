# QuickStart Guide

# To import package
```
from roam import Client
```

# To get locations for all users at project level
```
client = Client(API_KEY=<API-KEY>)
```

# To get locations for one user
```
client = Client(API_KEY=<API-KEY>, USER_ID=<USER-ID>)
```

# To get locations for a list of users under the same project
```
USER_LIST = ["user_id1", "user_id2", ...]
client = Client(API_KEY=<API-KEY>, USER_ID=<USER_LIST>)
```

# To get locations from a group of users
```
client = Client(API_KEY=<API-KEY>, GROUP_ID=<GROUP_ID>)
```

# To start listening to locations
```
client.sub()
```

# To stop listening to locations
```
client.disconnect()
```

By default the SDK prints out the locations. If the locations are required to any other output, then
please use a callback function. 

# Define callback function and pass in client initialization
```
def custom_callback_function(payload):
    # print(payload)
    # save_to_file(payload)
    # log(payload)

client = Client(API_KEY=<API-KEY>, CALLBACK=<custom_callback_function>)
```