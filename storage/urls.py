from django.urls import path

from .views import (
      DashboardView,
      FolderDetailView,
      FolderCreateView,
      FolderDeleteView,
      FileUploadView,
      FileRenameView,
      FileDeleteView,
)
app_name = "storage"

urlpatterns = [
      path("",DashboardView.as_view(),name="dashboard",),
      path("folder/<int:pk>/",FolderDetailView.as_view(),name="folder-detail",),
      path("folder/create/",FolderCreateView.as_view(),name="folder-create",),
      path("folder/<int:pk>/delete/",FolderDeleteView.as_view(),name="folder-delete",),
      path("folder/<int:folder_id>/upload/",FileUploadView.as_view(),name="file-upload",),
      path("file/<int:pk>/rename/",FileRenameView.as_view(),name="file-rename",),
      path("file/<int:pk>/delete/",FileDeleteView.as_view(),name="file-delete",),
]