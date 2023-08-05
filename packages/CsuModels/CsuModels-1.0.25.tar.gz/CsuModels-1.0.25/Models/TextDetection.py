from PMTD.model import PMTD


class TextDetection:
    def __init__(self, merge_from_file, model_path):
        self.model = PMTD(merge_from_file=merge_from_file, model_path=model_path)

    def train(self, images_path, results_path):
        self.model.train(images_path=images_path, results_path=results_path)

