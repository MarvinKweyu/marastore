
#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

su -m myuser -c "rm /tmp/celerybeat-doshi.pid > /dev/null"

su -m myuser -c "celery beat -A maradomadstore.celery -l info --pidfile=/tmp/*.pid"