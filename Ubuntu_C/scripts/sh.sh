curl 'http://192.168.15.10:5000/'
curl -X PUT -d number=5 192.168.15.10:5000/number
curl -X POST -d 'command=reboot' http://192.168.15.10:5000/command