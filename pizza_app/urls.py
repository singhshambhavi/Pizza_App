from django.urls import path, include
from rest_framework.routers import SimpleRouter
from pizza_app import views

router_obj = SimpleRouter()
router_obj.register("pizza", views.PizzaView, basename="pizza")
urlpatterns = [
    path("pizza/list", views.PizzaList.as_view()),
    path('', include(router_obj.urls)),
]