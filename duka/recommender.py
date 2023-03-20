import redis
from django.conf import settings

from duka.models import Product

# connect to redis

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


class Recommender(object):
    """Recommend a product based on previous purchases"""

    def get_product_key(self, id):
        """
        Build redis key
        Example: product:33:purchased_with in product of id 33
        Parameters
        ----------
        id: int
            Id of a product

        """
        return f"product:{id}:purchased_with"

    def products_bought(self, products):
        """All products bought in the same Order
        Parameters
        ----------
        products: list
            A list of all products bought together i.e in the same Order
        """
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # get other products bought with each product
                if product_id != with_id:
                    # increment the score for products purchased together

                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products: list = [], max_results: int = 6):
        """Retrieve products bought together for a list of given products
        Parameters
        ----------

        products: list
            A list of Product objects to get recommendations for
        max_results: int
            The maximum number of recommendations to return
        """
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # one product
            # get ids of products that were bought with the given product ordered by the number of times they were bought together
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_results]
        else:
            # create temp key
            flat_ids = "".join([str(id) for id in product_ids])
            tmp_key = f"tmp_{flat_ids}"
            # multiple products, combine scores of all of them
            # store result in temp key
            keys = [self.get_product_key(id) for id in product_ids]
            # combine sum of all scores for items in sorted set of each product
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            # i.e if searching for recommendations for product xyz and product xyz is contained as one of the items being recommended, remove it
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove temporary key
            r.delete(tmp_key)
        suggested_product_ids = [int(id) for id in suggestions]
        # get prodcts and sort by order of appearence
        suggested_products = list(Product.objects.filter(id__in=suggested_product_ids))
        suggested_products.sort(key=lambda x: suggested_product_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        """Clear recommendations"""
        for id in Product.objects.values_list("id", flat=True):
            r.delete(self.get_product_key(id))
