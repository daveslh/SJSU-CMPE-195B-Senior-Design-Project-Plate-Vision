import cv2
import boto3
import base64
from datetime import datetime
from io import BytesIO
from picamera2 import Picamera2
from PIL import Image

# AWS S3 configurations
S3_BUCKET_NAME = 'bucket-name'
VIDEO_STREAM_URL = 'websocket-url'  # For live stream to front-end

# Initialize AWS S3 client
s3_client = boto3.client('s3')

# Initialize Pi Camera
camera = Picamera2()
camera_config = camera.create_still_configuration(main={"size": (1280, 720)})
camera.configure(camera_config)
camera.start()

def upload_frame_to_s3(frame, filename):
    """Uploads the captured frame to an S3 bucket in PNG format."""
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image = image.resize((640, 640))
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=f"frames/{filename}.png",
        Body=buffer,
        ContentType='image/png'
    )
    print(f"Uploaded {filename}.png to S3.")

def stream_frame_to_frontend(frame):
    """Sends the live frame to the front-end via WebSocket."""
    encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
    base64_frame = base64.b64encode(encoded_frame).decode('utf-8')
    payload = {
        "action": "send_frame",
        "frame": base64_frame
    }
    # Simulate WebSocket send using a POST request
    response = requests.post(
        VIDEO_STREAM_URL,
        json=payload
    )
    print(f"Sent frame to front-end: {response.status_code}")

def process_video_stream():
    """Processes the video stream to detect motion and stream live frames."""
    prev_frame = None
    print("Starting video stream processing...")

    while True:
        # Capture the current frame
        frame = camera.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Initialize the previous frame if not set
        if prev_frame is None:
            prev_frame = gray
            continue

        # Motion detection
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = any(cv2.contourArea(c) >= 1000 for c in contours)

        # Upload frame to S3 if motion detected
        if motion_detected:
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            upload_frame_to_s3(frame, filename)

        # Stream live video frame to the front-end
        stream_frame_to_frontend(frame)

        # Update the previous frame for the next iteration
        prev_frame = gray

try:
    process_video_stream()
except KeyboardInterrupt:
    print("Stopping camera.")
    camera.stop()
