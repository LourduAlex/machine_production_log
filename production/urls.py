
from django.urls import path
from .views import RegisterView, LoginView, CreateEditProductionLogView, DeleteProductionLogView, ProductionLogListView

urlpatterns =[

    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', LoginView.as_view(), name='login'),
    path('production-log/', CreateEditProductionLogView.as_view(), name='production-log'),
    path('production-log/<int:pk>/', CreateEditProductionLogView.as_view(), name='production-log-edit'),
    path('production-log/<int:id>', DeleteProductionLogView.as_view(), name='production-log-delete'),
    path('productionlog-list/', ProductionLogListView.as_view(), name='production-log-list'),

]

