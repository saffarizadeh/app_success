import os
import cv2
import json
import numpy as np

class ImageDataset(object):
    def __init__(self, train_path):
        self.train_path = train_path
        self.image_filenames = os.listdir(train_path)

    def load_image(self, file_path):
        return cv2.imread(file_path)

    def get_image_arrays(self):
        return np.array([self.load_image(self.train_path + filename) for filename in self.image_filenames])

    def read_json_as_dict(self):
        with open('crawled_data.json', 'r') as f:
            return json.load(f)

    def get_image_lables(self):
        labels = []
        label_dataset = self.read_json_as_dict()
        for image_filename in self.image_filenames:
            rating_count = label_dataset[image_filename[:-4]]['userRatingCount']
            labels.append(rating_count)
        labels = np.array(labels)
        labels = (labels - np.mean(labels))/np.std(labels)
        return labels