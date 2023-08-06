# Response Report

Save the httpx-response from the server. This may be needed when debugging.

```python
from httpx import Client
from response_report import Reporter

client = Client()

response = client.get("https://pfel.cc/donate")

Reporter(response).save('donate_report.txt')
```