from django.conf.urls import url

from . import views

app_name = 'restocking'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^product_finder/$', views.ProductFinderView.as_view(), name='product_finder'),
    url(r'^product_finder/results/$', views.ProductFinderResults.as_view(), name='product_finder_results'),
    url(r'^nfc/$', views.NfcIndex.as_view(), name='nfc_index'),
    url(r'^nfc/find_nfc_devices/$', views.find_nfc_devices, name='find_nfc_devices'),
    url(r'^nfc/tag_encoder/pick_device$', views.NfcDevicePicker.as_view(), name='tag_encoder_pick_device'),
    url(r'^nfc/tag_identifier/pick_device$', views.NfcDevicePicker.as_view(), name='tag_identifier_pick_device'),
    url(r'^nfc/tag_identifier/(?P<device>\d+)$', views.nfc_identify, name='tag_identifier'),
    url(r'^nfc/tag_encoder/find_product/(?P<device>\d+)$', views.ProductFinderView.as_view(), name='tag_encoder_find_product'),
    url(r'^nfc/tag_encoder/pick_product$', views.ProductFinderResults.as_view(), name='tag_encoder_pick_product'),
    url(r'^nfc/tag_encoder/encode$', views.nfc_encode, name='tag_encoder'),

    #url(r'^nfc/tag_encoder/$', views.ProductFinderView.as_view(), name='tag_encoder'),
    #url(r'^nfc/tag_encoder/results/$', views.ProductFinderResults.as_view(), name='tag_encoder_results'),
    #url(r'^add_data/$', views.add_data, name='add_data'),DO NOT ENABLE THIS
]
