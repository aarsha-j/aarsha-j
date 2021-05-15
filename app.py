import os, io
from google.cloud import vision
import cv2
from time import sleep
import time
import pprint 
import anvil.server
from anvil.tables import app_tables

anvil.server.connect("YXN4MTSAQBMOFG2RFF2CVDS3-MCO3NAETCWJR5HK7")


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'GCVision.json' 
client = vision.ImageAnnotatorClient()
print("API setup")

def get_emotion_from_cloud(image_path):

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.face_detection(image=image)
    if(response.face_annotations[0].joy_likelihood == "Likelihood.value"):
        print("you look happy")
        hi = "happy"
        return hi
    hi = response.face_annotations[0].joy_likelihood
    new_row = app_tables.table.add_row(
                                            mood=str(response.face_annotations[0].joy_likelihood)
                                            )
    
    return hi


def get_image_from_frame(cap):
    ret, frame = cap.read()
    file = 'frame.png'
    cv2.imwrite(file,frame)
    cv2.imshow('frame',frame) #show camera output
    return file

def start_camera():

    cap = cv2.VideoCapture(0)
    print("Starting camera")

    while True:
        time_span = time.time + 5
        img = get_image_from_frame(cap)
        key = cv2.waitKey(0) #press 0 to move through frames

        if key == ord('q'): #press q to quit
            break
        elif key == ord('s'): #press s to see
            get_emotion_from_cloud(img)
    
    cap.release() #release the object when the app quits.
    cv2.destroyAllWindows()


start_camera()