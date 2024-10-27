from chromadb.api.types import QueryResult

from apps.store.recommendations.chroma_client import collection


def upsert_product(prod_title: str, prod_id: int, metadata: dict) -> None:
    """
        Update the embeddings, metadatas or documents for provided ids,
        or create them if they don't exist
    """

    collection.upsert(
        documents=[prod_title],
        ids=[str(prod_id)],
        metadatas=[metadata]
    )

    return None


def get_recommendations(
    prod_category: str,
    prod_name: str,
    n_results: int = 4,
    same_category: bool = False,
) -> QueryResult:
    """
    Retrieve product recommendations based on the given product name and
    category.
    ---
    Args:
        prod_category (str): The category of the product to filter by.
        prod_name (str): The name of the product to find recommendations for.
        n_results (int, optional): The number of results to return.
        same_category (bool, optional): Whether to include products in the same category.

    Returns:
        QueryResult: The result of the query containing recommended products.
    """

    condition = {
        "category": {
            "$in" if same_category else "$nin": [prod_category]
        }
    }

    result = collection.query(
        query_texts=[prod_name],
        n_results=n_results,
        where=condition
    )

    return result


def get_similar(
    query: str,
    n_results: int = 4,
    prod_category: str = None,
    add_condition: bool = True,
    same_category: bool = True,
) -> QueryResult:
    """
    Retrieve products similar to the given query. Optionally, add a filter
    condition based on the product category.
    ---
    Args:
        prod_category (str): The category of the product to filter by.
        query (str): The query text to find similar products.
        n_results (int, optional): The number of results to return.
        add_condition (bool, optional): Whether to add a filter condition.
        same_category (bool, optional): Whether to include products in the same category.

    Returns:
        QueryResult: The result of the query.
    """

    if add_condition:
        if not prod_category:
            raise ValueError(
                'Product category is required when adding a condition'
            )
        condition = {
            "category": {
                "$in" if same_category else "$nin": [prod_category]
            }
        }
    else:
        condition = None

    result = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=condition
    )

    return result
