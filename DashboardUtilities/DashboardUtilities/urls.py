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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^MatchMeters/$', views.match_meters),
    url(r'^GetBlocks/$',views.get_blocks),
)
