from Sort.model import Sort


class Tracking:
    def __init__(self, model_path, anchors_path,
                 classes_path, model_filename,
                 model_type, video_path, result_path):
        self.model = Sort(model_path=model_path, anchors_path=anchors_path,
                          classes_path=classes_path, model_filename=model_filename,
                          model_type=model_type, video_path=video_path,
                          result_path=result_path)

    def train(self):
        self.model.train()
