from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'restocking'
urlpatterns = [
    #AdminNavigation
    path('', views.IndexView.as_view(), name='index'),
    path('product_finder', views.ProductFinderView.as_view(), name='product_finder'),
    
    #AdminFunctions
    path('product_finder/results', views.ProductFinderResults.as_view(), name='product_finder_results'),

    #Rest
    #Order
    path('rest/order/<int:pk>', views.DetailsViewOrder.as_view(), name='details_order_date'),
    path('rest/order/<slug:delivery_date>', views.DetailsViewOrderByDate.as_view(), name='details_order_date_by_product'),
    #OrderItem
    path('rest/order_item/create', views.CreateOrderItemView.as_view(), name='create_order_item'),
    #Product
    path('rest/product/<int:pk>', views.DetailsViewProduct.as_view(), name='details_product'),

    #Forbidden Functions - Do not enable these unless you know what you're doing
    #path('forbidden/add_quantities', views.add_quantities, name='add_quantities'),
    #path('forbidden/add_data', views.add_data, name='add_data'),
    
]