from django.urls import path
from .views import upload_csv, history, generate_pdf,dataset_detail

urlpatterns = [
    path('upload/', upload_csv),
    path('history/', history),
    path('pdf/', generate_pdf),
     path('dataset/<int:dataset_id>/', dataset_detail),
]
