import os
from imagekitio import ImageKit

imagekit = ImageKit(
    private_key=os.environ['IMAGEKIT_PRIVATE_KEY'],
    public_key=os.environ['IMAGEKIT_PUBLIC_KEY'],
    url_endpoint='https://ik.imagekit.io/' + os.environ['IMAGEKIT_ID']
)

def upload_image(file_path: str, file_name: str):

  # upload to imagekit for storage
  upload_result = imagekit.upload_file(
      file=open(file_path, "rb"),
      file_name=file_name,
  )

  # return url
  return upload_result.url
