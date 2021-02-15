from rest_framework.routers import SimpleRouter

from .views import QuestionViewSet

router = SimpleRouter()
router.register("support", QuestionViewSet)

urlpatterns = router.urls
