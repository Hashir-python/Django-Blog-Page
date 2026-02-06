from .models import Category
from assignments.models import SocialSites


def get_categories(request):
    categories=Category.objects.all()
    return dict(categories=categories)

def get_Social_Links(request):
    Social=SocialSites.objects.all()
    return dict(Social=Social)