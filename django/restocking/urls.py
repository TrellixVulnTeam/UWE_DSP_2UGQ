from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'restocking'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^product_finder/$', views.ProductFinderView.as_view(), name='product_finder'),
    url(r'^product_finder/results/$', views.ProductFinderResults.as_view(), name='product_finder_results'),
    url(r'^nfc/$', views.NfcIndex.as_view(), name='nfc_index'),
    url(r'^nfc/find_nfc_devices/$', views.find_nfc_devices, name='find_nfc_devices'),
    url(r'^nfc/tag_encoder/pick_device$', views.NfcDevicePicker.as_view(), name='tag_encoder_pick_device'),
    url(r'^nfc/tag_encoder/encode$', views.nfc_encode, name='tag_encoder'),
    url(r'^nfc/tag_identifier/pick_device$', views.NfcDevicePicker.as_view(), name='tag_identifier_pick_device'),
    url(r'^nfc/tag_identifier/(?P<device>\d+)$', views.nfc_identify, name='tag_identifier'),
    url(r'^nfc/tag_encoder/find_product/(?P<device>\d+)$', views.ProductFinderView.as_view(), name='tag_encoder_find_product'),
    url(r'^nfc/tag_encoder/pick_product$', views.ProductFinderResults.as_view(), name='tag_encoder_pick_product'),

    url(r'^rest/order/(?P<pk>[0-9]+)/$', views.DetailsViewOrder.as_view(), name='details_order'),
    url(r'^rest/order/(?P<delivery_date>[\w\-]+)/$', views.DetailsViewOrderByDate.as_view(), name='details_order_date'),
    url(r'^rest/order/(?P<delivery_date>[\w\-]+)/(?P<product_id>[0-9]+)/$', views.DetailsViewOrderByDateFilterProduct.as_view(), name='details_order_date_by_product'),

    url(r'^rest/order_item/create$', views.CreateOrderItemView.as_view(), name='create_order_item'),
    
    url(r'^rest/product/(?P<pk>[0-9]+)/$', views.DetailsViewProduct.as_view(), name='details_product'),

    url(r'^skus$', views.skus, name='skus'), #DO NOT ENABLE THIS
    #url(r'^add_quantities$', views.add_quantities, name='add_quantities'), #DO NOT ENABLE THIS
    #url(r'^add_data/$', views.add_data, name='add_data'),DO NOT ENABLE THIS
]
