from django.contrib import admin

from .models import Folder, File


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
      list_display = (
            "name",
            "owner",
            "parent",
            "created_at",
            "updated_at",
      )

      list_filter = (
            "created_at",
            "updated_at",
      )

      search_fields = (
            "name",
            "owner__username",
      )


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
      list_display = (
            "original_name",
            "owner",
            "folder",
            "file_type",
            "size",
            "uploaded_at",
      )

      list_filter = (
            "file_type",
            "uploaded_at",
      )

      search_fields = (
            "original_name",
            "owner__username",
      )