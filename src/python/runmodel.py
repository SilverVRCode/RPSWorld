import asyncio
import json
import cv2
from ultralytics import YOLO
import websockets

model = YOLO("best copy.pt")

connected_clients = set()

async def register(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def broadcast_gestures():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame, verbose=False)

        detections = []
        for result in results:
            for box in result.boxes:
                detections.append({"label": result.names[int(box.cls[0])], "confidence": float(box.conf[0]), "box": box.xyxy[0].tolist()})

            if detections and connected_clients:
                message = json.dumps({"type": "gesture", "data": detections})

                await asyncio.gather(*[client.send(message) for client in connected_clients])

            await asyncio.sleep(0.01)

    cap.release()

async def main():
    async with websockets.serve(register, "localhost", 8765):
        print("websocket server started on ws://localhost:8765 :D")
        await broadcast_gestures()

if __name__ == "__main__":
    asyncio.run(main())