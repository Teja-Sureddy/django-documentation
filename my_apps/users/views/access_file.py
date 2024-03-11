from django.views import View
from django.http import HttpResponseForbidden, HttpResponse, FileResponse, HttpResponseNotFound
from my_project.settings import MEDIA_URL
import os
import mimetypes


class AccessFileView(View):
    def get(self, request, filename, directory='public', user_id=''):
        if request.user.id != user_id and directory != 'public':
            return HttpResponseForbidden("You do not have permission.")

        file_path = os.path.join(MEDIA_URL, f'{directory}/{user_id}/{filename}'.replace('//', '/'))
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
