import urllib.request
import urllib.error
import re

try:
    response = urllib.request.urlopen('http://127.0.0.1:8000/api/')
    print(response.read().decode())
except urllib.error.HTTPError as e:
    content = e.read().decode()
    # Find patterns
    patterns = re.findall(r'<li>(.*?)</li>', content)
    print("URL Patterns found:")
    for p in patterns:
        print(p)
except Exception as e:
    print(f"Error: {e}")
