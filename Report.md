# Отчёт
# Конфигурирование HostName и создание пользователя

1. Для начала создаём три виртуальные машины

![](./Laba/Screen/Screenshot_1.png)

2. Сконфигурируем HostName (для Ubuntu_B) с помощью команды

```shell 
$ sudo hostnamectl set-hostname primak_gateway
$ sudo nano /etc/hostname 
```
![](./Laba/Screen/Screenshot_8.png)

3. После этого добавляем ещё одного пользователя
```shell 
$ sudo adduser primak_2
```
![](./Laba/Screen/Screenshot_7.png)

4. Перезагружаем машину. Тоже самое проделываем с Ubuntu_С.
Меняем название хоста на primak_client. Добавляем пользователя primak_3

# Конфигурирование виртуального интерфейса

1. Заполняем конфигурационный файл
```shell 
$ sudo vim /etc/netplan/00-installer-config.yaml
```
2. Ubuntu - A

![](./Laba/Screen/Screenshot_25.png)

3. Проверяем на корректность и сохраняем файл

```shell 
$ sudo netplan --debug generate
$ sudo netplan apply
```
4. Ubuntu - B

![](./Laba/Screen/Screenshot_26.png)

5. Ubuntu - C

![](./Laba/Screen/Screenshot_27.png)

# Настройка шлюза

1. Разрешаем переброс пакетов на шлюзе

```shell 
$ sudo echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward 1
```
Теперь server и client видят друг друга через шлюз. Раскомментируем данную строку: net.ipv4.ip_forward=1 в файле,
чтобы при перезапуске машин шлюз восстанавливал видимость

```shell 
$  sudo vim /etc/sysctl.conf 
```

![](./Laba/Screen/Screenshot_19.png)

2. Настравиваем маршрут

```shell 
$ sudo iptables -A FORWARD -i enp0s9 -o enp0s8 -p tcp --syn --dport 5000 -m conntrack --ctstate NEW -j ACCEPT

$ sudo iptables -A FORWARD -i enp0s9 -o enp0s8 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
$ sudo iptables -A FORWARD -i enp0s8 -o enp0s9 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

$ sudo iptables -P FORWARD DROP

```

3. Сохраняем правила

```shell 
$ sudo apt-get install iptables-persistent
$ sudo iptables-save > /etc/iptables/rules.v4
$ sudo ip6tables-save > /etc/iptables/rules.v6
```
![](./Laba/Screen/Screenshot_20.png)


# Cервер

1. Создаём скрипт на python

![](./Laba/Screen/Screenshot_29.png)

2. С помощью systemd создаём сервис, который запускает скрипт через автозагрузку

```shell 
$ sudo vim /lib/systemd/system/web-server.service
```
3. Записываем следующий скрипт

![](./Laba/Screen/Screenshot_22.png)

4. Перезапускаем службу и активируем автозагрузку 

```shell 
$ sudo systemctl daemon-reload
$ sudo systemctl start web-server
$ sudo systemctl enable web-server
$ sudo systemctl status web-server
```

![](./Laba/Screen/Screenshot_23.png)


# Проверка работы 

1. на клиенте прописываем команды 

```shell 
$ curl 'http://192.168.15.10:5000/'
$ curl -X PUT -d number=5 192.168.15.10:5000/number
$ curl -X POST -d 'command=reboot' http://192.168.15.10:5000/command
```
![](./Laba/Screen/Screenshot_30.png)

2. Посмотрим на tcpdump

```shell 
$ sudo tcpdump -i enp0s9 tcp
```
![](./Laba/Screen/Screenshot_33.png)

![](./Laba/Screen/Screenshot_32.png)

Как видно из результатов запроса, у нас есть настройка на фильтрацию пакетов по порту


