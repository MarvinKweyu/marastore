
#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

su -m myuser -c "celery worker -A maranomadstore.celery -l info"