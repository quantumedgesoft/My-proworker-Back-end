from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_title = "MyProWorker"
admin.site.site_header = "MyProWorker"
admin.site.app_index = "Welcome to MyProWorker"

# setup 404 page
# handler404 = "home.views.error_404"
# handler500 = "home.views.error_500"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('authentication.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
