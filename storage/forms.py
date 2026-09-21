from django import forms
from .models import Folder, File

class FolderForm(forms.ModelForm):
      class Meta:
            model = Folder
            fields = ["name","parent",]
            widgets = {
                  "name": forms.TextInput(
                        attrs={
                              "class": "form-control",
                              "placeholder": "Enter folder name",
                        }
                  ),
                  "parent": forms.Select(
                              attrs={
                                    "class": "form-select",
                              }
                        ),
            }
      
      def __init__(self, *args, user = None, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.fields["parent"].queryset = Folder.objects.filter(owner = user ).order_by("name")
            self.fields["parent"].required = False

class FileUploadForm(forms.ModelForm):

      class Meta:
            model = File
            fields = [
                  "file",
            ]

            widgets = {
                  "file": forms.ClearableFileInput(
                  attrs={
                        "class": "form-control",
                  }
                  ),
            }

      def save(self, commit=True):

            instance = super().save(commit=False)

            uploaded_file = self.cleaned_data["file"]

            instance.original_name = uploaded_file.name

            instance.file_type = getattr(
                  uploaded_file,
                  "content_type",
            ) or ""

            instance.size = uploaded_file.size

            if commit:
                  instance.save()

            return instance
      
class FileRenameForm(forms.ModelForm):
      class Meta:
            model = File
            fields = ["original_name",]
            widgets = {
                  "original_name": forms.TextInput(
                  attrs={
                        "class": "form-control",
                        "placeholder": "Enter new file name",
                  }
                  ),
            }