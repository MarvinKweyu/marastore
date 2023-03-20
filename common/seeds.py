"""
This module seeds data across the project
"""

from django_seed import Seed
from faker import Faker


from duka.models import Category, Product

seeder = Seed.seeder("en_US")


def main():
    """Populate the DB"""
    seeder.entity(Category, 10)
    seeder.entity(Product, 20)


if __name__ == "__main__":
    main()
