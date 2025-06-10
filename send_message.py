import requests
from azure.storage.blob import BlobServiceClient,ContentSettings
from PIL import Image
from ultralytics import YOLO
from datetime import date
LINE_TOKEN = "W+X+1271FXB8uaNodQHuZP5tW8J3yAhuaFSeFu9HDY1HBhrQO4Rltj9SqiHt1AAGu8aUYtkFqf3DO/EpNIhE7hFRud+Gd+tWlb24HsN48r7CUtfWr4Nmy8w5lrj6cHYmVQMzu2HmLsU/Dgxk/JuqIwdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "Uc212577a1d485dd5cc08f1e97f32118a"

conn_str="DefaultEndpointsProtocol=https;AccountName=diseaseimages;AccountKey=r/u6nBt8xtk/l4jiyxKDmAwKzJMO+h/qEEZrR90rqI6jH0PYHiH4kNR2OTIAzKAsjb0mkRcNj5Nf+AStfTJhMg==;EndpointSuffix=core.windows.net"
container_name="images"

def upload_image(local_file_path,blob_name):
     blob_service_client = BlobServiceClient.from_connection_string(conn_str)
     container_client = blob_service_client.get_container_client(container_name)
     blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
     with open(local_file_path,"rb") as data:
          blob_client.upload_blob(data,overwrite=True)
          url=blob_client.url

     return url

class LINEBOT:
        def __init__(self,LINE_TOKEN,LINE_USER_ID):
            self.LINE_TOKEN=LINE_TOKEN
            self.LINE_USER_ID=LINE_USER_ID
            self.API="https://api.line.me/v2/bot/message/push"
            self.headers={
                        "Content_Type": "application/json",
                        "Authorization": "Bearer "+ self.LINE_TOKEN
            }
        def send_message(self,message):
            data = {
              "to":self.LINE_USER_ID,
              "messages":[{
                  "type": "text",
                  "text": message
              }]
            }
            requests.post(self.API, headers=self.headers, json=data).json()

            print("LINE message sent successfully ")
            return # Exit the loop on successful send
 
        def send_image(self,image_url):
            data={
                "to":self.LINE_USER_ID,
                "messages":[{
                        "type":"image",
                        "originalContentUrl":image_url,
                        "previewImageUrl":image_url
                }]
            }
            requests.post(self.API,headers=self.headers,json=data).json()

            print("LINE image sent successfully")
            return

model=YOLO("last.pt")
results=model("images/test/images/20240825_062542916_iOS.jpg",conf=0.5,stream=True)
for result in results:
     result_img=result.plot()
     img = Image.fromarray(result_img[..., ::-1])
     img.save("result.jpg",quality=50,optimize=True)
LINEBOT=LINEBOT(LINE_TOKEN,LINE_USER_ID)
LINEBOT.send_message("test")
LINEBOT.send_image(upload_image("result.jpg",f"{date.today()}.jpg"))