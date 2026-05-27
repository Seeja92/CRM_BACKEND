
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    NoteViewSet,
    CallViewSet,
    TaskViewSet,
    MeetingViewSet,
    EmailViewSet,
    make_call,end_call,
)

router = DefaultRouter()

router.register(r'notes', NoteViewSet, basename='notes')
router.register(r'calls', CallViewSet, basename='calls')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'meetings', MeetingViewSet, basename='meetings')
router.register(r'emails', EmailViewSet, basename='emails')

urlpatterns = [
    path('make-call/', make_call),
    path('end-call/', end_call),
]

urlpatterns += router.urls