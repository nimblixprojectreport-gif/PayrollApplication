import urllib.request
import urllib.error

url = 'http://127.0.0.1:8000/api/leave-types/'
print(f"Testing URL: {url}")
try:
    with urllib.request.urlopen(url) as response:
        print(f"Status: {response.getcode()}")
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"Status: {e.code}")
    print(e.read().decode()[:500])
except Exception as e:
    print(f"Error: {e}")
