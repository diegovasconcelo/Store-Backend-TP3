from typing import Tuple

from apps.store.models import (
    Sale,
    Product,
    RecommendationItem,
    Recommendation
)

from apps.store.recommendations.recommendation_service import (
    get_similar,
    get_recommendations,
)


def get_similar_objects(
    query: str,
    add_condition: bool = False,
    product_category: str = None,
    same_category: bool = True,
    n: int = 4,
) -> Tuple[Product, dict]:
    """
    Retrieve similar products based on a query string.
    ---
    Args:
        query (str): The search query to find similar products.
        add_condition (bool, optional): Whether to add an additional condition
            based on product category. Defaults to False.
        product_category (str, optional): The category of the product to
            filter by when add_condition is True.
        same_category (bool, optional): Whether to restrict results to the same
            category.
        n (int, optional): The number of similar products to retrieve.

    Returns:
        Tuples[Product, dict]: A tuple containing a queryset of similar Product
            objects and a dictionary with additional result information.

    Raises:
        ValueError:
            If `add_condition` True and `product_category` is not provided.
    """

    if add_condition and not product_category:
        raise ValueError(
            'product_category is required when add_condition is True'
        )

    result = get_similar(
        query=query,
        n_results=n,
        prod_category=product_category,
        add_condition=add_condition,
        same_category=same_category,
    )
    ids = result.get('ids', [])[0]

    return Product.objects.filter(id__in=ids), result


def get_recomendations_objects(
    prod_category: str,
    query: str,
    same_category: bool = False,
    n: int = 4,
) -> Tuple[Product, dict]:
    """
    Retrieve recommended product based on a given category and query.

    Args:
        prod_category (str): The category of the product to base
            recommendations on.
        query (str): The name or identifier of the product to query
            recommendations for.
        same_category (bool, optional): If True, restrict recommendations
             to the same category.
        n (int, optional): The number of recommendations to retrieve.

    Returns:
        Tuple[Product, dict]: A tuple containing a queryset of recommended
            Product objects and a dictionary with recommendation details.
    """

    result = get_recommendations(
        prod_category,
        prod_name=query,
        n_results=n,
        same_category=same_category,
    )

    ids = result.get('ids', [])[0]

    return Product.objects.filter(id__in=ids), result


def create_recomendation(
    sale: Sale,
    same_category: bool = False,
    n_results: int = 4
) -> Recommendation:
    """
    Generates product recommendations based on a given sale.
    ---
    This function creates recommendations for products in a sale by finding
        similar products.
    It calculates a confidence score based on the distances of the
        recommended products and associates these recommendations
        with the sale.

    Args:
        sale (Sale): The sale object containing the products for which
            recommendations are to be generated.
        same_category (bool, optional): If True, recommendations will be
            limited to products in the same category. Defaults to False.
        n_results (int, optional): The number of similar products to retrieve
            for each product in the sale. Defaults to 4.

    Returns:
        Recommendation: The created recommendation object containing the
            recommended items and confidence score.
    """

    recomendations = []
    distances = []
    for product in sale.products.all():
        objs, similar_products = get_recomendations_objects(
            product.category.name,
            product.name,
            same_category=same_category,
            n=n_results,
        )

        # Take the objects of the products and the distances
        zip_objects = zip(objs, similar_products['distances'][0])
        for obj, distance in zip_objects:
            # Get or create the recommendation item
            r_item, r_item_created = RecommendationItem.objects.get_or_create(
                score=distance
            )
            if r_item_created:
                r_item.products.add(obj)
            distances.append(distance)
            recomendations.append(r_item)

    # Calculate the confidence score - the average of the distances
    confidence_score = sum(distances) / len(distances)

    # Create the recommendation object
    recommendation = Recommendation.objects.create(
        sale=sale,
        client=sale.client,
        confidence_score=round(confidence_score, 2),
    )
    recommendation.items.add(*recomendations)
    recommendation.save()

    return recommendation
