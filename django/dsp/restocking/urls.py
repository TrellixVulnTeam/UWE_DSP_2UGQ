from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'restocking'
urlpatterns = [
    ################
    #AdminNavigation
    ################
    path('administration', views.AdminIndexView.as_view(), name='admin_index'),
    path('administration/product_finder', views.ProductFinderView.as_view(), name='product_finder'),
    path('administration/product_finder/results', views.ProductFinderResults.as_view(), name='product_finder_results'),
    #Transactions
    path('administration/transactions', views.TransactionIndex.as_view(), name='transaction_index'),
    path('administration/transactions/product_finder', views.TransactionProductFinderView.as_view(), name='transaction_product_finder'),
    path('administration/transactions/product_finder/results', views.TransactionProductFinderResults.as_view(), name='transaction_product_finder_results'),
    path('administration/transactions/process_transaction', views.process_transaction, name='process_transaction'),

    #Data Creation
    #path('administration/data_creation/order_3000', views.create_order_3000, name='create_order_3000'),
    #path('administration/data_creation/transaction/<int:quantity>', views.create_transaction, name='create_transaction'),

    #ManagerNavigation
    path('manager', views.ManagerIndexView.as_view(), name='manager_index'),
    path('manager/deliveries', views.AskProcessDelivery.as_view(), name='ask_process_delivery'),
    path('manager/deliveries/<slug:delivery>', views.ResultsProcessDelivery.as_view(), name='results_process_delivery'),
    path('manager/deliveries/process/<slug:delivery_date>', views.process_delivery, name='process_delivery'),
    path('manager/orders/create', views.CreateOrder.as_view(), name='create_order'),

    #Rest
    #Order
    path('rest/order/<int:pk>/', views.DetailsViewOrder.as_view(), name='details_order_date'),
    path('rest/order/<slug:delivery_date>', views.DetailsViewOrderByDate.as_view(), name='details_order_date'),
    path('rest/order/<slug:delivery_date>/<int:product>', views.DetailsViewOrderByDateFilterProduct.as_view(), name='details_order_date_filter_product'),
    #OrderItem
    path('rest/order_item/create', views.CreateOrderItemView.as_view(), name='create_order_item'),
    #Product
    path('rest/product/<int:pk>/', views.DetailsViewProduct.as_view(), name='details_product'),
    #RestockingList
    path('rest/restocking/<int:pk>/', views.DetailsViewRestocking.as_view(), name='details_restocking'),
    path('rest/restocking/<slug:date>/<slug:time>', views.DetailsViewRestockingByTime.as_view(), name='details_restocking_time'),
    path('rest/restocking/<slug:date>/<slug:time>/<int:product>', views.DetailsViewRestockingByTimeFilterProduct.as_view(), name='details_restocking_time_filter_product'),
    path('rest/restocking/latest', views.get_latest_restocking, name='get_latest_restocking'),
    path('rest/restocking/create', views.generate_restocking_list, name='generate_restocking_list'),
    #Recommend
    path('rest/recommend/<int:item>', views.recommend, name='recommend'),
    path('rest/recommend/remove/<int:item>', views.remove_from_restocking, name='remove_from_restocking'),
    path('rest/test/test', views.rest_test, name='rest_test'),

    #Forbidden Functions - Do not enable these unless you know what you're doing
    #path('forbidden/add_quantities', views.add_quantities, name='add_quantities'),
    #path('forbidden/add_data', views.add_data, name='add_data'),
    #path('forbidden/add_floor_quantities', views.add_floor_quantities, name='add_floor_quantities'),
]
