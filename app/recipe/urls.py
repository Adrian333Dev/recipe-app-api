# URL mapping for recipe app

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

# Create a router object
router = DefaultRouter()
# Register the recipe viewset with the router
router.register('recipes', views.RecipeViewSet)

# Define the app name
app_name = 'recipe'

urlpatterns = [
    # Register the router with the urlpatterns
    path('', include(router.urls))
]
