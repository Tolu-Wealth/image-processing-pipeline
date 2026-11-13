
import boto3
import os
import io
from urllib.parse import unquote_plus
from PIL import Image

s3 = boto3.client("s3")
DEST_BUCKET = os.environ["DEST_BUCKET"]


def lambda_handler(event, context):
    try:
        # Handle automatic S3 upload events
        if "Records" in event:
            record = event["Records"][0]
            bucket = record["s3"]["bucket"]["name"]
            key = unquote_plus(record["s3"]["object"]["key"])

        # Handle EventBridge events
        elif "detail" in event:
            bucket = event["detail"]["bucket"]["name"]
            key = event["detail"]["object"]["key"]

        # Handle direct tests and Step Functions/API Gateway requests
        else:
            bucket = event["bucket"]
            key = event["key"]

        print(f"Source bucket: {bucket}")
        print(f"Source image: {key}")
        print(f"Destination bucket: {DEST_BUCKET}")

        # Download original image
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response["Body"].read()

        # Resize image
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((200, 200))

        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        # Save resized image as JPEG
        output = io.BytesIO()
        image.save(output, format="JPEG")
        output.seek(0)

        # Create output filename
        filename = key.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        resized_key = f"thumbnails/{filename}_thumbnail.jpg"

        # Upload resized image
        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=resized_key,
            Body=output.getvalue(),
            ContentType="image/jpeg"
        )

        print(f"Successfully uploaded: {resized_key}")

        return {
            "status": "SUCCESS",
            "message": "Image resized successfully",
            "output_bucket": DEST_BUCKET,
            "output_key": resized_key
        }

    except Exception as e:
        print(f"Image processing failed: {str(e)}")
        raise
