from django.urls import path

from .views import GetTagView, GetTagsView

app_name = "api"

urlpatterns = [
    path("tags/", GetTagsView.as_view(), name="tags"),
    path("tags/<int:id>/", GetTagView.as_view(), name="tag"),
]
