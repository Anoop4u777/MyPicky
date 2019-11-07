from django.conf.urls import url
from restaurants.views import (
					RestaurantCreate,
					RestaurantList,
					RestaurantDetail,
					RestaurantUpdate
						)


urlpatterns = [
    url(r'^create/$', RestaurantCreate.as_view(), name='create'),
    url(r'^list/$', RestaurantList.as_view(), name='list'),
    url(r'^list/(?P<slug>[\w-]+)/$', RestaurantUpdate.as_view(), name='detail'),
    #url(r'^list/(?P<slug>[\w-]+)/edit/$', RestaurantUpdate.as_view(), name='edit'),
]
