
#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

su -m myuser -c "celery worker -A maradomadstore.celery -l info"