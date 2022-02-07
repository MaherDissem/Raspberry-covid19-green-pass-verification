import cv2
import pyzbar.pyzbar as pyzbar
import json
import zlib
import base45
import cbor2
from cose.messages import CoseMessage
import json
import time
import requests

camera = cv2.VideoCapture(0)

def decodeDisplay(image):    
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    codes = pyzbar.decode(gray)
    print('reading...', end='\r')

    data=dict()
    for code in codes:
        codeData = code.data.decode()
        codeType = code.type
        decoded = base45.b45decode(codeData[4:])
        decompressed = zlib.decompress(decoded)
        cose = CoseMessage.decode(decompressed)
        data=json.loads(json.dumps(cbor2.loads(cose.payload), indent=2))
    return image, data

try:
 cv2.namedWindow("preview", cv2.WND_PROP_FULLSCREEN)    
 cv2.setWindowProperty("preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
 cv2.startWindowThread()
   
 while True:
# Read current frame
  ret, frame = camera.read()
  
  cv2.imshow("preview", frame)
  
  try:
      im, data = decodeDisplay(frame)
  except:
      # QR code is not green pass
      im=cv2.putText(im, "INVALID", (180,250), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 3, cv2.LINE_AA)
      cv2.imshow("preview", im)
      time.sleep(4)
  
  if data:
      payload = {'dgc': data['1']}
      r = requests.get('http://localhost:3000/', params=payload)
      #print('Return code: ', r.status_code, ', Text: ', r.text)

      # Valid pass
      if r.status_code == 200:
          # get data
          family_name = data['-260']['1']['nam']['fn']
          first_name = data['-260']['1']['nam']['gn']
          date_of_birth = data['-260']['1']['dob']
          issuing_country = data['1']
          
          # calculate center of image
          font=cv2.FONT_HERSHEY_SIMPLEX
          textsize=cv2.getTextSize(family_name, font, 1, 2)[0]
          textX=(im.shape[1]-textsize[0])//2
          textY=(im.shape[0]+textsize[1])//2
          
          # display data
          im=cv2.putText(im, first_name, (textX,textY), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_AA)
          im=cv2.putText(im, family_name, (textX,textY+100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_AA)
          im=cv2.putText(im, date_of_birth, (textX,textY+200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2, cv2.LINE_AA)
          
          cv2.imshow("preview", im)
          time.sleep(4)
          
      else:
        im=cv2.putText(im, "INVALID", (180,250), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 3, cv2.LINE_AA)
        cv2.imshow("preview", im)
        time.sleep(4)
except KeyboardInterrupt:
 print('interrupted!')
