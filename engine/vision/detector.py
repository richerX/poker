from ultralytics import YOLO
from ultralytics.yolo.engine import results


# Yolo v8 detection
class Detector:
    pretrained_model = "vision/playing_cards_2.pt"

    def __init__(self):
        self.model = YOLO(self.pretrained_model)

    def detect(self, filepath, save = True) -> dict[str, float]:
        cards: dict[str, float] = dict()
        output: list[results] = self.model(filepath, save = save, verbose = False)
        for box in output[0].boxes:
            class_name: str = self.model.names.get(int(box.cls))
            confidence: float = float(box.conf)
            cards[class_name] = max(confidence, cards.get(class_name, 0))
        return cards
