from django.db.models import Avg
from .models import Category, Product


def category_ids(root_category):
    ids = [root_category.id]
    for child in root_category.subcategories.all():
        ids += category_ids(child)
    return ids

def average_price_for_category(category):
    ids = category_ids(category)
    return Product.objects.filter(category__in=ids).aggregate(avg_price=Avg('price'))['avg_price'] or 0

from .models import Category

def get_or_create_category_by_path(path):
    if not path:
        return None

    parent = None
    category = None

    for name in path:
        # Either get an existing category or create a new one under the parent
        category, _ = Category.objects.get_or_create(
            name=name,
            defaults={"parent": parent},
        )

        # Update parent for the next iteration
        parent = category

    return category
