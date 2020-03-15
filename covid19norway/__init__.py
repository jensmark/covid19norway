from importlib import import_module
from os import makedirs, path


class Dataset:
    def __init__(self, source: str):
        self.source = import_module(f'covid19norway.source.{source}')

    def json(self):
        return self.source.json()

    def csv(self):
        return self.source.csv()

    def save(self, folder):
        def save_dataset(sub_folder, dataset, ext=''):
            makedirs(path.join(folder, sub_folder), exist_ok=True)
            for k, v in dataset.items():
                with open(path.join(folder, sub_folder, f'{k}.{ext}'), 'w') as f:
                    f.write(v)

        save_dataset('json', self.json(), 'json')
        save_dataset('csv', self.csv(), 'csv')
