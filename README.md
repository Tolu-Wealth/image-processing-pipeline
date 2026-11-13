# Serverless Image Processing Pipeline

## 1. Project Overview

This project is a serverless image processing pipeline built using Amazon Web Services (AWS). It automatically resizes uploaded images and stores the resized versions in a separate Amazon S3 bucket.

The project uses AWS Lambda to process images, AWS Step Functions to coordinate the workflow, and Amazon API Gateway to provide an HTTP endpoint for starting image-processing executions.

## 2. Technologies Used

- **Amazon S3:** Stores original and resized images.
- **AWS Lambda:** Processes and resizes images using Python.
- **AWS Step Functions:** Manages the image-processing workflow.
- **Amazon API Gateway:** Provides an HTTP POST endpoint to start the workflow.
- **Python:** Implements the image-resizing logic.
- **Pillow:** Python library used for image manipulation.

## 3. Project Architecture

The processing workflow is:

An original image is stored in the source S3 bucket.
A request is sent to the API Gateway endpoint with the source bucket name and image key.
API Gateway starts the Step Functions state machine.
Step Functions invokes the ImageResizeFunction Lambda function.
Lambda retrieves the original image from S3.
Pillow resizes the image to a maximum dimension of 200 × 200 pixels.
The resized image is saved in the destination S3 bucket under the thumbnails/ folder.
Step Functions checks the processing result and reports success or failure.

## 4. AWS Resources

| Resource | Name |
|---|---|
| AWS Region | ca-central-1 |
| Source S3 Bucket | tolulope-original-images |
| Destination S3 Bucket | tolulope-resized-images |
| Lambda Function | ImageResizeFunction |
| Step Functions State Machine | ImageProcessingStateMachine |
| API Gateway | ImageProcessingAPI |
| API Resource | /process-image |
| HTTP Method | POST |
| Deployment Stage | prod |

## 5. Repository Files

- `lambda_function.py` – Python source code for resizing images.
- `statemachine.asl.json` – AWS Step Functions workflow definition.
- `test-event.json` – Sample input used to test the workflow.
- `requirements.txt` – Python dependency list.

## 6. Setup Instructions

### Step 1: Create S3 Buckets

Create two S3 buckets in the same AWS region:

- `tolulope-original-images`
- `tolulope-resized-images`

The first bucket stores original images, while the second stores processed images.

### Step 2: Create the Lambda Function

1. Create a Lambda function named `ImageResizeFunction`.
2. Select a Python runtime.
3. Upload the deployment package containing `lambda_function.py` and the compatible Pillow library.
4. Set the handler to `lambda_function.lambda_handler`.
5. Configure the environment variable:

   - Key: `DEST_BUCKET`
   - Value: `tolulope-resized-images`

6. Give the Lambda execution role permission to read objects from the source bucket and write objects to the destination bucket.

### Step 3: Create the Step Functions State Machine

1. Open AWS Step Functions.
2. Create a Standard state machine.
3. Use the definition in `statemachine.asl.json`.
4. Replace the Lambda ARN in the definition with the ARN of your own Lambda function.
5. Ensure the state machine execution role has permission to invoke the Lambda function.

### Step 4: Configure API Gateway

1. Create a REST API named `ImageProcessingAPI`.
2. Create a resource named `/process-image`.
3. Create a POST method.
4. Configure the integration to start the Step Functions execution using `StartExecution`.
5. Configure the integration request to pass the state machine ARN and request body.
6. Give API Gateway permission to start executions of the state machine.
7. Deploy the API to a stage named `prod`.

### Step 5: Test the Pipeline

Send a POST request to the API Gateway endpoint with this JSON body:

```json
{
  "bucket": "tolulope-original-images",
  "key": "your-image-file.jpg"
}
```

Replace `your-image-file.jpg` with the name of an image stored in the source bucket.

After the execution succeeds, check the destination S3 bucket for the resized image inside the `thumbnails/` folder.

## 7. Sample Test Input

The repository includes `test-event.json`, which contains the sample input used during development and testing.

## 8. Expected Output

The resized image is stored in the destination bucket using this naming format:

`thumbnails/original_filename_thumbnail.jpg`

The image is resized while maintaining its aspect ratio, with a maximum dimension of 200 × 200 pixels.

## 9. Error Handling

The Step Functions workflow checks the result returned by Lambda.

- Successful processing moves to the Success state.
- Failed processing moves to the Failure state.

## 10. Conclusion

This project demonstrates how AWS serverless services can work together to build an automated image-processing pipeline. It uses cloud storage, event-driven processing, workflow orchestration, and API integration without requiring a continuously running server.
