from ultralytics import YOLO
import cv2

# load the default pretrained YOLOv11n (trained on COCO)
model = YOLO("best copy.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)      # runs COCO detection out of the box
    annotated = results[0].plot()

    cv2.imshow("YOLOv11n COCO Demo", annotated)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()