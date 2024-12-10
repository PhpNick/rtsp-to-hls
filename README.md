# Docker-окружение для сервера, преобразующего RTSP в HLS

## Установка и запуск

Откройте терминал, перейдите в папку с `docker-compose.yml` и запустите:

```
docker-compose up -d
```

С использованием параметра --build:

```
docker-compose up -d --build
```

### Остановка и удаление контейнеров

Чтобы остановить и удалить контейнеры используйте команду `down`:

```
docker-compose down
```

### Пример запроса к серверу

```
curl -X POST http://localhost:5000/convert -H "Content-Type: application/json" -d '{"rtsp_url": "rtsp://your_rtsp_link"}'
```

Ответ

```
{
  "hls_link": "/output/<unique_id>/output.m3u8"
}
```

Итоговая ссылка на видео

```
http://localhost:5000/output/<unique_id>/output.m3u8
```