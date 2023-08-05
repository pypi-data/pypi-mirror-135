from django.conf.urls import url, include
from enrichapp.dashboard.control.urls import control_urlpatterns
from enrichapp.dashboard.audit.urls import audit_urlpatterns
from enrichapp.dashboard.catalog.urls import catalog_urlpatterns
from enrichapp.dashboard.persona.urls import persona_urlpatterns
from enrichapp.dashboard.filerenderer.urls import filerenderer_urlpatterns
from enrichapp.dashboard.marketplace.urls import marketplace_urlpatterns, get_marketplace_urls

from . import views, control, catalog

app_name = "APPNAME"

# => Base
urlpatterns = [
    url('^[/]?$', views.index, name="index"),

]

urlpatterns += [
    url(r'^control/', include((control_urlpatterns,"control"),
                              namespace="control"),
        {
            'spec': control.get_spec()
        })
]

urlpatterns += [
    url(r'^catalog/', include((catalog_urlpatterns,'catalog'),
                              namespace="catalog"),
        {
            'spec': catalog.get_spec()
        })
]


# Enable it
#from . import persona
#searchspec = persona.get_spec()
#urlpatterns += [
#    url(r'^persona/', include((persona_urlpatterns, "persona"),
#                               namespace="persona"),
#        {
#            'spec': searchspec
#        })
#]
