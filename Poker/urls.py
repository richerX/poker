from django.contrib import admin
from django.urls import path
from app.views import index_page, generator_page, visor_page, predictor_page, predictor_get_predictions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('generator/', generator_page),
    path('predictor/', predictor_page),
    path('predictor/get_predictions', predictor_get_predictions),
    path('visor/', visor_page),
]
