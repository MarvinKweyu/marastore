# [The Traveller's Store](https://www.marvinkweyu.net/projects/the_travellers_store)

The Traveller's Shopping experience


![The Traveller](./screens/marastorereview.gif)
- [The Traveller's Store](#the-travellers-store)
  - [Core features](#core-features)
  - [Setup](#setup)
    - [Setting up a Braintree account](#setting-up-a-braintree-account)
    - [Bare metal](#bare-metal)
      - [Base requirements](#base-requirements)
      - [Running message brokers;](#running-message-brokers)
    - [Sample credit card details to test with:](#sample-credit-card-details-to-test-with)
    - [Docker](#docker)



An article around the build process can be found on [marvinkweyu/themarastore](https://www.marvinkweyu.net/projects/the_travellers_store)
## Core features
:heavy_check_mark: Viewing items in the shop

:heavy_check_mark: Filtering items by category

:heavy_check_mark: Managing your cart

:heavy_check_mark: Email notifcations on order

:heavy_check_mark: Credit card payment

:heavy_check_mark: Generate PDF invoice on sale and send the invoice to the customer

:heavy_check_mark: Recommendation engine for products that go well with others


## Setup
---

### Setting up a Braintree account

This solution uses [Braintree](https://www.braintreepayments.com/) for payment. Create your account on the [developer](https://sandbox.braintreegateway.com) portal and get the sandbox keys. Once done, modify the `base.py` settings file in the config folder.

```python
# PAYMENTS
BRAINTREE_CONF = braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id=env("BRAINTREE_MERCHANT_ID"),
    public_key=env("BRAINTREE_PUBLIC_KEY"),
    private_key=env("BRAINTREE_PRIVATE_KEY"),
)

```

### Bare metal
#### Base requirements

Install the following dependencies **before** running the `develop` bash script.

- [Postgresql](https://www.postgresql.org/download/)
- [RabbitMQ](https://www.rabbitmq.com/download.html)
- [Redis](https://redis.io/)
- [Weasyprint](https://weasyprint.org/)

Setup a virtual environment, install requirements , run migrations and run the server

```bash
bash develop.sh
```

#### Running message brokers;
Launch rabbitMQ on terminal 1
```bash
sudo rabbitmq-server
```
On a different terminal, launch celery

```bash
celery -A maranomadstore worker -l info
```

To monitor asynchronous tasks i.e task statistics
```bash
celery -A maranomadstore flower
```
Then access the task list queue on *localhost:5555*

Access the project via: **127.0.0.1:8000**



### Sample credit card details to test with:

*Credit card numbers*
- 4111111111111111
- 4005519200000004
- 4012000033330026

*Sample CVC* - 123

Key in any data in the future as the expiration date

**Example:**
12/2030

---
### Docker

**Development**

With *docker* and *docker-compose* installed , clone the repo and run the following command at the root of the project.
```bash
docker-compose -f local.yaml up -d --build
```

Access the project via: **127.0.0.1:8000**
