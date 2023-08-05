import csv
import os

from pype import utils


class ResultsCollector():
    def __init__(self, fieldnames):
        pipeline_dir = utils.get_pipeline_dir()

        self.path = os.path.join(pipeline_dir, 'results.csv')
        self.fieldnames=fieldnames
        with open(self.path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    def write(self, results):
        with open(self.path, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(results)
