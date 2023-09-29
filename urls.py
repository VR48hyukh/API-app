from django.urls import path
from .import views
from django.urls import path
from . import views as v


urlpatterns = [
	path('', v.index, name='index'),
	path('list_all_products/', v.list_all_products, name='list_all_products'),
	path('items_from_product/', v.items_from_product, name='items_from_product'),
	path('total/', v.total, name='total')
]