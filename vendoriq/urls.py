from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vendor.urls')),
    # Namespace Django's built-in auth URLs to avoid colliding with our app's
    # own `login`/`logout` URL names (templates use `{% url 'login' %}`).
    path('accounts/', include(('django.contrib.auth.urls', 'accounts'), namespace='accounts')),
]
