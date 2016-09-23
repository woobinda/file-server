# Задача
Сделать файловый сервер, который будет использоваться сервисами `myownradio` и в будущем `radioteria`.

## Зачем
Существующий сервер обладает рядом ограничений. В нем нет авторизации, поэтому каждый мог бы слать 
запросы на сервер и заливать/удалять файлы беспрепятственно. Поэтому заливка происходит не напрямую, а
через бекенд-сервер.

## Что должно получиться
Маленький `stand-alone` файловый сервер, запускаемый из командной строки и конфигурируемый ключами при запуске.

Пример команды запуска сервера:

```
server.py \
  --port 80 \
  --hash-algo sha-1 \
  --content-dir /path/to/files \
  --private-token d41d8cd98f00b204e9800998ecf8427e
```

Ключ `--port` определяет на каком порту сервер должен слушать соединения, 
ключ `--hash-algo` определяет алгоритм хеширования, по которому будет определяться хеш файла,
ключ `--content-dir` определяет папку, в которой будут содержаться загруженные файлы, и
ключ `--private-token` определяет секретный ключ, служащий защитой от вандализма.
