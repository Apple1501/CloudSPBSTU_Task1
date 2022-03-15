curl 'http://192.168.15.10:5040/'
curl -X PUT -d number=5 192.168.15.10:5040/number
curl -X POST -d 'command=reboot' http://192.168.15.10:5040/command