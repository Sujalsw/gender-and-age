import cv2

# Function to detect faces and draw bounding boxes
def faceBox(faceNet, frame):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    
    # Create input blob for the network
    blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227), [104, 117, 123], swapRB=False)
    
    # Set the input for the neural network
    faceNet.setInput(blob)
    
    # Run the forward pass to get face detections
    detection = faceNet.forward()
    
    bbox = []
    for i in range(detection.shape[2]):
        confidence = detection[0, 0, i, 2]
        
        # If confidence is above 0.7, consider the detection as a face
        if confidence > 0.7:
            x1 = int(detection[0, 0, i, 3] * frameWidth)
            y1 = int(detection[0, 0, i, 4] * frameHeight)
            x2 = int(detection[0, 0, i, 5] * frameWidth)
            y2 = int(detection[0, 0, i, 6] * frameHeight)
            
            # Append bounding box coordinates
            bbox.append([x1, y1, x2, y2])
            
            # Draw the bounding box on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green color, thickness 2

    return frame ,bbox


# Load face detection model
faceProto = r"C:\Users\sujal\OneDrive\Desktop\projects\gender and age detection\opencv_face_detector.pbtxt"
faceModel = r"C:\Users\sujal\OneDrive\Desktop\projects\gender and age detection\opencv_face_detector_uint8.pb"

ageProto = r"C:\Users\sujal\OneDrive\Desktop\projects\gender and age detection\age_deploy.prototxt"
ageModel = r"C:\Users\sujal\OneDrive\Desktop\projects\gender and age detection\age_net.caffemodel"

genderProto  = r"C:\Users\sujal\OneDrive\Desktop\projects\gender and age detection\gender_deploy.prototxt"
genderModel = r"C:\Users\sujal\OneDrive\Desktop\projects\gender and age detection\gender_net.caffemodel"

faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel,genderProto)


ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']


# Start video capture from the webcam
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    # Detect faces and draw bounding boxes
    frame, bbox= faceBox(faceNet, frame)
    MODEL_MEAN_VALUES = [78.4263377603, 87.7689143744, 114.895847746]

    for bbox in bbox:
        face = frame[bbox[1]:bbox[3],bbox[0]:bbox[2]]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (227, 227),MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPred = genderNet.forward()
        gender = genderList[genderPred[0].argmax()]


        ageNet.setInput(blob)
        agePred = ageNet.forward()
        age = ageList[agePred[0].argmax()]

        label = "{},{}".format(gender,age)
        cv2.putText(frame, label, (bbox[0],bbox[1]-10),cv2.FONT_HERSHEY_COMPLEX,0.8, (255,255,255),2)


    # Display the video with detected faces
    cv2.imshow("age-gender", frame)

    # Check if 'q' key is pressed to quit
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# Release the video capture and close all OpenCV windows
video.release()
cv2.destroyAllWindows()
