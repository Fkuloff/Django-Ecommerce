from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('_nested_admin/', include('nested_admin.urls')),

                  path('', include('apps.main.urls')),
                  path('catalog/', include('apps.store.urls')),
                  path('cart/', include('apps.cart.urls')),
                  path('accounts/', include('apps.accounts.urls')),
                  path('orders/', include('apps.order.urls')),
                  path('review/', include('apps.review.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
