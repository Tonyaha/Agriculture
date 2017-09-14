import socket

host = 'github.com'

try:
    with open('/etc/hosts', 'a+') as fp:
        ip = socket.gethostbyname(host)
        fp.write(' '.join([ip, host, '\n']))
except BaseException as e:
    print(e)
else:
    print('sucess')