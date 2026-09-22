from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView,CreateView
from .forms import FolderForm, FileRenameForm, FileUploadForm

from .models import File, Folder

class DashboardView(LoginRequiredMixin, ListView):
      model = Folder
      template_name = "storage/dashboard.html"
      context_object_name = "folders"

      def get_queryset(self):
            return Folder.objects.filter(
                  owner=self.request.user,
                  parent__isnull=True,
            ).order_by("name")

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            user = self.request.user

            # All folders belonging to the logged-in user
            all_folders = Folder.objects.filter(owner=user)

            # All files belonging to the logged-in user
            all_files = File.objects.filter(owner=user)

            context["total_folders"] = all_folders.count()
            context["total_files"] = all_files.count()

            # File type statistics
            context["image_count"] = all_files.filter(
                  file_type__startswith="image/"
            ).count()

            context["video_count"] = all_files.filter(
                  file_type__startswith="video/"
            ).count()

            context["audio_count"] = all_files.filter(
                  file_type__startswith="audio/"
            ).count()

            context["pdf_count"] = all_files.filter(
                  file_type="application/pdf"
            ).count()

            context["document_count"] = all_files.filter(
                  file_type__in=[
                  "application/msword",
                  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                  ]
            ).count()

            context["presentation_count"] = all_files.filter(
                  file_type__in=[
                  "application/vnd.ms-powerpoint",
                  "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                  ]
            ).count()

            context["total_storage"] = sum(
                  file.size for file in all_files
            )

            return context
            
class FolderDetailView(LoginRequiredMixin, DetailView):
      model = Folder
      template_name = "storage/folder_details.html"
      context_object_name = "folder"
      
      def get_queryset(self):
            return Folder.objects.filter(owner = self.request.user)
      
      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["subfolders"] = self.object.children.filter(
                  owner=self.request.user
            ).order_by("name")

            context["files"] = self.object.files.filter(
                  owner=self.request.user
            ).order_by("-uploaded_at")
            return context

class FolderDeleteView(LoginRequiredMixin, DeleteView):
      model = Folder
      template_name = "storage/folder_confirm_delete.html"

      def get_queryset(self):
            return Folder.objects.filter(
                  owner=self.request.user
            )

      def get_success_url(self):
            return reverse_lazy("storage:dashboard")
      
class FolderCreateView(LoginRequiredMixin, CreateView):

      model = Folder
      form_class = FolderForm
      template_name = "storage/folder_form.html"

      def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()

            kwargs["user"] = self.request.user

            return kwargs

      def get_initial(self):
            initial = super().get_initial()

            parent_id = self.request.GET.get("parent")

            if parent_id:
                  try:
                        parent = Folder.objects.get(
                              pk=parent_id,
                              owner=self.request.user,
                        )

                        initial["parent"] = parent

                  except Folder.DoesNotExist:
                        pass

            return initial

      def form_valid(self, form):

            form.instance.owner = self.request.user

            messages.success(
                  self.request,
                  "Folder created successfully."
            )

            return super().form_valid(form)

      def get_success_url(self):

            if self.object.parent:
                  return self.object.parent.get_absolute_url()

            return reverse_lazy("storage:dashboard")

class FileUploadView(LoginRequiredMixin, CreateView):

      model = File
      form_class = FileUploadForm
      template_name = "storage/file_upload.html"

      def dispatch(self, request, *args, **kwargs):

            self.folder = get_object_or_404(
                  Folder,
                  pk=self.kwargs["folder_id"],
                  owner=request.user,
            )

            return super().dispatch(
                  request,
                  *args,
                  **kwargs
            )

      def form_valid(self, form):

            form.instance.owner = self.request.user
            form.instance.folder = self.folder

            messages.success(
                  self.request,
                  "File uploaded successfully."
            )

            return super().form_valid(form)

      def get_context_data(self, **kwargs):

            context = super().get_context_data(**kwargs)

            context["folder"] = self.folder

            return context

      def get_success_url(self):

            return self.folder.get_absolute_url()

class FileRenameView(LoginRequiredMixin, UpdateView):
      model = File
      form_class = FileRenameForm
      template_name = "storage/file_rename.html"

      def get_queryset(self):
            return File.objects.filter(
                  owner=self.request.user
            )

      def get_success_url(self):

            return self.object.folder.get_absolute_url()

class FileDeleteView(LoginRequiredMixin, DeleteView):

      model = File
      template_name = "storage/file_confirm_delete.html"

      def get_queryset(self):
            return File.objects.filter(
                  owner=self.request.user
            )

      def get_success_url(self):

            return self.object.folder.get_absolute_url()

class FolderRenameView(LoginRequiredMixin, UpdateView):
      model = Folder
      form_class = FolderForm
      template_name = "storage/folder_details.html"
      context_object_name = "folder"

      def get_queryset(self):
            return Folder.objects.filter(
                  owner=self.request.user
            )

      def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs["user"] = self.request.user
            return kwargs

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            context["subfolders"] = self.object.children.filter(
                  owner=self.request.user
            ).order_by("name")

            context["files"] = self.object.files.filter(
                  owner=self.request.user
            ).order_by("-uploaded_at")

            context["rename_mode"] = True

            return context

      def get_success_url(self):
            return self.object.get_absolute_url()
            model = Folder
            form_class = FolderForm
            template_name = "storage/folder_rename.html"

            def get_queryset(self):
                  return Folder.objects.filter(
                        owner=self.request.user
                  )

            def get_form_kwargs(self):
                  kwargs = super().get_form_kwargs()
                  kwargs["user"] = self.request.user
                  return kwargs

            def get_success_url(self):
                  return self.object.get_absolute_url()