from django.views import View
from django.http import HttpResponseForbidden, HttpResponse, FileResponse, HttpResponseNotFound
from my_project import settings
import os
import mimetypes


class AccessFileView(View):
    def get(self, request, directory, user_id, filename):
        if request.user.id != user_id:
            return HttpResponseForbidden("You do not have permission.")

        file_path = os.path.join(settings.MEDIA_ROOT, f'{directory}/{user_id}/{filename}')
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = 'application/octet-stream'

        if content_type.startswith('image'):
            with open(file_path, 'rb') as f:
                return HttpResponse(f.read(), content_type=content_type)

        try:
            return FileResponse(open(file_path, 'rb'), content_type=content_type)
        except FileNotFoundError:
            return HttpResponseNotFound("File not found.")
