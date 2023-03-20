# The MaraNomads Store

The MaraNomads Shopping experience


- [The MaraNomads Store](#the-maranomads-store)
  - [Core features](#core-features)
  - [Setup](#setup)
    - [Bare metal](#bare-metal)
      - [Base requirements](#base-requirements)
      - [Running message brokers;](#running-message-brokers)
    - [It just works(Docker)  - WIP](#it-just-worksdocker----wip)


## Core features
:heavy_check_mark: Viewing items in the shop

:heavy_check_mark: Filtering items by category

:heavy_check_mark: Adding items to the cart and viewing the cart

:heavy_check_mark: Sending an email confirmation on order

:heavy_check_mark: Complete payment of order using a credit card

:heavy_check_mark: Generate PDF invoice on sale and send the invoice to the customer

:heavy_check_mark: Recommendation engine for products that go well with others


## Setup 
---

### Bare metal
#### Base requirements

Install the following dependencies before running the `develop` bash script.

- Postgresql
- RabbitMQ
- Weasyprint

Setup a virtual environment, install requirements , run migrations and run the server

```bash
bash develop.sh
```

#### Running message brokers;
Launch rabbitMQ
```bash
sudo rabbitmq-server
```
On a different terminal, launch celery

```bash
celery -A maradomadstore worker -l info

```

To monitor asynchronous tasks i.e task statistics
```bash
celery -A maradomadstore flower
```
Then access the task list queue on *localhost:5555*
### It just works(Docker)  - WIP

**Development**

With *docker* and *docker-compose* installed , clone the repo and run the following command at the root of the project.
```bash
docker-compose -f docker-compose.yml up -d --build

```

**Production**

```bash
docker-compose -f docker-compose.prod.yml up -d --build

```

Access the project via: **127.0.0.1:8000**