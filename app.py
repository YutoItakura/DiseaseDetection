from flask import Flask,request
from flask_cors import CORS
from PIL import Image
from ultralytics import YOLO
import cv2
from azure.storage.blob import BlobServiceClient,ContentSettings
import io
from datetime import date

conn_str="DefaultEndpointsProtocol=https;AccountName=diseaseimages;AccountKey=r/u6nBt8xtk/l4jiyxKDmAwKzJMO+h/qEEZrR90rqI6jH0PYHiH4kNR2OTIAzKAsjb0mkRcNj5Nf+AStfTJhMg==;EndpointSuffix=core.windows.net"
container_name="images"

def upload_image(image_buffer,blob_name):
     blob_service_client = BlobServiceClient.from_connection_string(conn_str)
     container_client = blob_service_client.get_container_client(container_name)
     blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
     content_settings = ContentSettings(content_type="image/jpeg")
     blob_client.upload_blob(image_buffer, overwrite=True, content_settings=content_settings)

app=Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "ファイルが見つかりません", 400

    file = request.files["file"]
    minetype=file.content_type
    if minetype.startswith("image/"):
     img=cv2.imread(file)
     model=YOLO('last.pt')
     results=model(img,conf=0.5 ,show_conf=False,show_labels=False, stream=True)
     for result in results:
        result_img=result.plot()
        img = Image.fromarray(result_img[..., ::-1])
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=50, optimize=True)
        buffer.seek(0)
        upload_image(buffer,f"api{date.today()}.jpg")

        return "uploaded successfully"
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)