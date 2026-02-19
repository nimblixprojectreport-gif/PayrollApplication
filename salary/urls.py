from rest_framework.routers import DefaultRouter
from .views import SalaryComponentViewSet, SalaryStructureViewSet

router = DefaultRouter()
router.register(r'salary-components', SalaryComponentViewSet)
router.register(r'salary-structures', SalaryStructureViewSet)

urlpatterns = router.urls
