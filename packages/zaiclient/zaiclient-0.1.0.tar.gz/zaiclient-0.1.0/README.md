# Z.ai Client SDK

Z.ai official client SDK.

Z.ai clients can utilize this package to easily authenticate and connect to Z.ai's machine learning API endpoint.



## Example Usage

```python
import zaiclient

client = zaiclient.ZaiClient('test', SECRET_TOKEN)
client.get_recommendations(user, history)
```

