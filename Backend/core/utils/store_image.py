import logging
import boto3
from botocore.exceptions import ClientError
import uuid
from dao.article.image import Image

log = logging.getLogger(__name__)


def upload_request_files(request_files):
    saved_images = []

    cover_image = request_files['cover_image']
    images = request_files.getlist('images')

    # Upload cover image
    cover_image_uuid = str(uuid.uuid4())
    upload_file(cover_image, 'lra', cover_image_uuid, cover_image.mimetype)
    saved_images.append(Image(is_cover=True, storage_id=cover_image_uuid))

    # Upload other images
    for image in images:
        image_uuid = str(uuid.uuid4())
        upload_file(image, 'lra', image_uuid, image.mimetype)
        saved_images.append(Image(is_cover=False, storage_id=image_uuid))

    return saved_images


def upload_file(image_file, bucket, filename, content_type):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(
            Body=image_file, Bucket=bucket, Key=filename, ContentType=content_type, ACL='public-read')
    except ClientError as e:
        log.error(f'Error during image upload: {e}')
        return False
    return True
