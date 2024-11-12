import insightface
import numpy as np
from PIL import Image
import cv2

# Загрузка моделей с использованием CPUExecutionProvider
app = insightface.app.FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

# Укажите путь к вашей модели замены лиц ONNX
model_path = 'models/inswapper_128.onnx'
swapper = insightface.model_zoo.get_model(model_path, providers=['CPUExecutionProvider'])

def read_image(file):
    image = Image.open(file)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def preprocess_face(image, face_bbox):
    x1, y1, x2, y2 = [int(c) for c in face_bbox]
    face = image[y1:y2, x1:x2]
    face = cv2.resize(face, (128, 128))
    face = face.astype(np.float32)
    face = np.expand_dims(face, axis=0)
    return face

def swap_faces(src_img, tgt_img):
    src_faces = app.get(src_img)
    tgt_faces = app.get(tgt_img)

    if len(src_faces) == 0 or len(tgt_faces) == 0:
        return None, "No faces detected in one or both images."

    # Используем первую найденную пару лиц для замены
    src_face = src_faces[0]
    tgt_face = tgt_faces[0]

    # Замена лиц с помощью модели
    swapped_face_img = swapper.get(tgt_img, src_face, tgt_face)

    return swapped_face_img, None
