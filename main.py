import numpy as np
import cv2
import requests
import time 
import json
import urllib.request

cap = cv2.VideoCapture(0)



    # Capture frame-by-frame
while(True):
    try:
        feeling = "neutral"

        ret, frame = cap.read()

        stt = cv2.imencode('.jpg', frame )[1].tostring()
        print("photo")

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        header = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '88c5ffe8f93f4b45a184aea33acc88d3',
        }

        res = requests.post(url='https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize',
                            data=stt,
                            headers=header)

        # Display the resulting frame
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        max = 0.0
        # print (res)
        datajson = res.json()
        print (datajson)
        params = ""
        if len(datajson) > 0:
            if float(datajson[0]["scores"]["happiness"]) > 0.15:
                max = float(datajson[0]["scores"]["happiness"])
                feeling = "happy"
                print(feeling)
            if float(datajson[0]["scores"]["anger"]) > 0.15 and float(datajson[0]["scores"]["anger"]) > max:
                max = float(datajson[0]["scores"]["anger"])
                feeling = "angry"
                print(feeling)
            if float(datajson[0]["scores"]["fear"]) > 0.15 and float(datajson[0]["scores"]["fear"]) > max:
                max = float(datajson[0]["scores"]["fear"])
                feeling = "fear"
                print(feeling)

            if float(datajson[0]["scores"]["sadness"]) > 0.15 and float(datajson[0]["scores"]["sadness"]) > max:
                max = float(datajson[0]["scores"]["sadness"])
                feeling = "sad"
                print(feeling)

            if float(datajson[0]["scores"]["surprise"]) > 0.15 and float(datajson[0]["scores"]["surprise"]) > max:
                max = float(datajson[0]["scores"]["surprise"])
                feeling = "surprise"
                print(feeling)

            if float(datajson[0]["scores"]["disgust"]) > 0.15 and float(datajson[0]["scores"]["disgust"]) > max:
                max = float(datajson[0]["scores"]["disgust"])
                feeling = "disgust"
                print(feeling)
            
            paramsPat = "happy" + "=" + str(datajson[0]["scores"]["happiness"])
            paramsPat += "&angry" + "=" + str(datajson[0]["scores"]["anger"])
            paramsPat += "&fear" + "=" + str(datajson[0]["scores"]["fear"])
            paramsPat += "&sad" + "=" + str(datajson[0]["scores"]["sadness"])
            paramsPat += "&surprise" + "=" + str(datajson[0]["scores"]["surprise"])
            paramsPat += "&disgust" + "=" + str(datajson[0]["scores"]["disgust"])


            urllib.request.urlopen("http://pathos.scalingo.io/setDoctorStatusAll?"+paramsPat).read()

        time.sleep(3)

        if max == 0.0:
            continue

        last = feeling

        urllib.request.urlopen("http://pathos.scalingo.io/setDoctorStatus?status="+feeling).read()
    except KeyboardInterrupt:
        raise
    except:
        pass    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
