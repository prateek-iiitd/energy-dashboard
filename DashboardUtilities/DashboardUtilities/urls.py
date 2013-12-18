from django.conf.urls import patterns, include, url
from RateChangeUtility import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DashboardUtilities.views.home', name='home'),
    # url(r'^DashboardUtilities/', include('DashboardUtilities.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.choose_meters),
    url(r'^GetBlocks/$',views.get_blocks),
    url(r'^GetWings/$',views.get_wings),
    url(r'^GetFloors/$',views.get_floors),
    url(r'^MatchResults/$',views.matching_meters),
    url(r'^PollingRate/$',views.polling_rate),
    url(r'^DownloadOptions/',views.download_options),
    url(r'^logout/$',views.logout),
    url(r'^login-error/$', views.error),
)
