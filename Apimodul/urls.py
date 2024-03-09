from rest_framework.routers import SimpleRouter

from .views import ConsentView,FetchView

router = SimpleRouter()

router.register(r'Consent',ConsentView,basename='Consent')
router.register(r'FetchData',FetchView,basename='Fetchdata')
urlpatterns = router.urls