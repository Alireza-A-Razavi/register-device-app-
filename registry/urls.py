from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("order.urls")),
    path("", include("account.urls")),
    path("", include("products.urls")),
    path('private-media/', include("private_storage.urls")),
] 

urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
