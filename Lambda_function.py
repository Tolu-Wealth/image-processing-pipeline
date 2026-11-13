
import boto3
import os
import io
from PIL import Image

s3 = boto3.client("s3")

DEST_BUCKET = os.environ["DEST_BUCKET"]

def lambda_handler(event, context):
    try:
        # Get the original image information
        if "detail" in event:
            bucket = event["detail"]["bucket"]["name"]
            key = event["detail"]["object"]["key"]
        else:
            bucket = event["bucket"]
            key = event["key"]

        # Download original image
        response = s3.get_object(
            Bucket=bucket,
            Key=key
        )

        image_data = response["Body"].read()

        # Open and resize image
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((200, 200))

        # Convert image to JPEG
        output = io.BytesIO()
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        image.save(output, format="JPEG")
        output.seek(0)

        # Save resized image
        filename = key.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        resized_key = f"thumbnails/{filename}_thumbnail.jpg"

        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=resized_key,
            Body=output.getvalue(),
            ContentType="image/jpeg"
        )

        return {
            "status": "SUCCESS",
            "message": "Image resized successfully",
            "output_bucket": DEST_BUCKET,
            "output_key": resized_key
        }

    except Exception as e:
        print(f"Image processing failed: {str(e)}")

        return {
            "status": "FAILED",
            "message": str(e)
        }
