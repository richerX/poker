from torch.hub import load
from ultralytics import YOLO
from ultralytics.yolo.engine import results


# Yolo v8 detection
class Detector:
    pretrained_model_v5 = "vision/v5.pt"
    pretrained_model_v8 = "vision/v8.pt"

    def __init__(self, version = "v5"):
        self.version = version
        if version == "v5":
            self.model = load("ultralytics/yolov5", "custom", self.pretrained_model_v5, verbose = False)
        elif version == "v8":
            self.model = YOLO(self.pretrained_model_v8)
        else:
            raise ValueError("Incorrect version, possible values - v5, v8.")

    def detect(self, filepath, save = True, threshold = 0) -> dict[str, float]:
        detections = []
        if self.version == "v5":
            detections = self._detect_v5(filepath, save)
        elif self.version == "v8":
            detections = self._detect_v8(filepath, save)

        cards: dict[str, float] = dict()
        for classname, confidence in detections:
            if confidence > threshold:
                cards[classname] = max(confidence, cards.get(classname, 0))
        return cards

    def _detect_v5(self, filepath, save) -> list[list[str, float]]:
        detections: list[list[str, float]] = []
        output = self.model(filepath)
        for value in output.pandas().xyxy[0].values:
            detections.append([value[-1], value[-3]])
        return detections

    def _detect_v8(self, filepath, save) -> list[list[str, float]]:
        detections: list[list[str, float]] = []
        output: list[results] = self.model(source = filepath, save = save, verbose = False)
        for box in output[0].boxes:
            detections.append([self.model.names.get(int(box.cls)), float(box.conf)])
        return detections
