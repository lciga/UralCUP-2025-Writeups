# Pyromancy | easy | web

## Информация

> Какие-то очередные "стартаперы" предложили нам внедрить их решение. Надо бы проверить его на безопасность...
> PS - название файла flag.txt
> http://5.1.53.43:5645/
> 5.1.53.43:5643
> 5.1.53.43:5644
## Описание



## Решение

1. На сайте заходим в документацию, где видим использование Pyro4, отсюда же видим список открытых функций. 

2. Изучив документацию к Pyro4, можно обнаружить инстурменты для управления сервером разрешения имен Pyro4. Используем его на данных портах, чтобы получить список доступных интерфейсов:
```bash
python3 -m Pyro4.nsc -n 5.1.53.43 -p 5643 list
#или
pyro4-nsc -n 5.1.53.43 -p 5643 list

#--------START LIST 
#Private --> PYRO:PrivateFunctions@0.0.0.0:5644
#Public --> PYRO:PublicFunctions@0.0.0.0:5644
#Pyro.NameServer --> PYRO:Pyro.NameServer@l0.0.0.0:9090
#    metadata: ['class:Pyro4.naming.NameServer']
#--------END LIST 
``` 


3. На http://5.1.53.43:5645/docs перичислены функции доступные на интерфейсе Public. Особое внимание стоит PrintInfo(). Для взаимодействия с сервером напишем небольшой клиент.
```python
import pyro4
public = "PYRO:PublicFunctions@5.1.53.43:5644"
private = "PYRO:PrivateFunctions@5.1.53.43:5644"
public_proxed = Pyro4.Proxy(public)
private_proxed = Pyro4.Proxy(private)
print(public_proxed.PrintInfo())
```

```bash
python3 client.py

# Hi, this is the Pyro project object management server. 
# If you registered at the website, you can manage your serialized objects here.
# Please consider, that not all of functional is implemented
# The functions are: 
# PrintInfo() - Returns this message
# CreateFreeUser() - Creates free user and returns it's token
# PutObject(unique_token:string, object:b64string ) - puts your object into db
# GetObjectList(unique_token:string) - returns your objects
# LoadObject(unique_token:string, object_name:string) - not implemented
# RemoveObject(unique_token:string, object_name:string) - not implemented
# StartObjectServer(unique_token:string, object_name:string) - not implemented
```

4. По аналогии с Public, можно попробовать вызвать PrintInfo() на интерфейсе Private:
```python
#...
print(private_proxed.PrintInfo())
```

```bash
python3 client.py

# Hi pal, i've temporarly disabled authentication here to add some of our objects from vacation
# Please don't forget to enable it again

# Hi, this is the Pyro project object management server administrative interface. 
# Be aware, that some functions can cause vulnerabilities
# Please consider, that not all of functional is implemented here, use configuration file to manage them
# The available functions are: 
# PrintInfo() - Returns this message
# DisablePickleCheck(unique_token:string) - Disables picklescan checking
# ForceRestartObject(object_uuid:uuid4) - Force Restarts object (better use local menu)
# ForceRemoveObject(object_uuid:uuid4) - Force remove object (better use local menu)
# Chcfg(cfgname:string, cfgvalue:json) - Remotely change configuration, changes may require restart (better use local menu)
```


5. Среди методов интерфейса замечаем "DisablePickleCheck", который отключает проверку пиклов перед загрузкой, но он требует токен администратора. Функция GetObjectList возвращает объекты пользователя по его токену. Все условия располагают к SQLi - ее и пробуем обнаружить и проэксплуатировать.
6. Используя интерфейс `Public` и метод `CreateFreeUser` создаем новго пользователя и получаем его токен.
7. В GetObjectList есть UNION-скуля, эксплуатируем ее, получаем токен админа
8. Вызываем DisablePickleCheck с токеном админа
9. Делаем базовый pickle-payload на ревшелл / отстук через curl и закидываем
10. Вы великолепны - читаем флаг!

[Решение, с помощью Python](solve/solve.py).

## Флаг

`TyumenCTF{3mbr4c3_7h3_fl4m3}`

