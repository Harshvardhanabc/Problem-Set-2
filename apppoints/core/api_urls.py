from rest_framework.routers import DefaultRouter
from .views import AppViewSet, TaskViewSet

router = DefaultRouter()
router.register('apps', AppViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = router.urls