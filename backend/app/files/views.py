from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
import uuid
import os
import tempfile
import requests
from shared.image_uploader import upload_image

class ImgUploadView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES['img_upload']  # should match the name of the PrimeVue component
        original_filename = file_obj.name
        unique_name = str(uuid.uuid4()) + original_filename

        # Save file locally in a temp directory
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in file_obj.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        # Upload the file to an external service
        uploaded_file_url = self.upload_to_external_service(temp_file_path, unique_name)

        # Clean up the local temp file
        os.remove(temp_file_path)

        return Response({'url': uploaded_file_url}, status=status.HTTP_200_OK)

    def upload_to_external_service(self, file_path, unique_name):
        # upload to imagekit for storage
        return upload_image(file_path, unique_name)
