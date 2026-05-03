from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/projects/list/',
                                  permanent=True), name='home'),
    path('projects/', include('teamfn.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls)
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
