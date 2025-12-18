import cv2
from ultralytics import YOLO

# Загружаем модель один раз
model = YOLO("yolov8n.pt")

face_model = YOLO("yolo_models/yolov8n-face-lindevs.pt")
plate_model = YOLO("yolo_models/license_plate_detector.pt")

# Классы, которые будем анонимизировать
TARGET_CLASSES = {
    "person",        # лица (упрощённо)
    "license plate"  # номера (если модель обучена)
}

def blur_boxes(image, boxes):
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        roi = image[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        blurred = cv2.GaussianBlur(roi, (221, 221), 0)
        image[y1:y2, x1:x2] = blurred

def anonymize_image(input_path: str, output_path: str):
    image = cv2.imread(input_path)

    # Детекция лиц
    face_results = face_model(image)[0]
    blur_boxes(image, face_results.boxes)

    # Детекция номеров
    plate_results = plate_model(image)[0]
    blur_boxes(image, plate_results.boxes)

    cv2.imwrite(output_path, image)