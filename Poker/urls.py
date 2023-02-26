from django.contrib import admin
from django.urls import path
from app.views import index_page, generate_mode_page, test_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('generator/', generate_mode_page),
    path('test/', test_page)
]
