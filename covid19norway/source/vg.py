from covid19norway.rawdata import download
from json import dumps
import pandas as pd
import numpy as np


SOURCE_MAP = {
    'allCases': 'https://www.vg.no/spesial/2020/corona-viruset/data/norway-allCases/',
    'casesByCounty': 'https://redutv-api.vg.no/corona/v1/sheets/norway-table-overview/?region=county',
    'casesByMunicipality': 'https://redutv-api.vg.no/corona/v1/sheets/norway-table-overview/?region=municipality',
    'casesByAge': 'https://redutv-api.vg.no/corona/v1/sheets/norway-age-data',
    'norwayData': 'https://redutv-api.vg.no/corona/v1/sheets/norway-region-data/'
}


def __raw_data():
    return {k: download(v) for k, v in SOURCE_MAP.items()}


def json():
    return {k: dumps(v, indent=2) for k, v in __raw_data().items()}


def csv():
    data = __raw_data()
    data['timeseriesNew'] = data['norwayData']
    data['timeseriesTotal'] = data['norwayData']
    data.pop('norwayData')

    return {k: __csv_mapper(k)(v) for k, v in data.items()}


def __csv_mapper(name: str):

    def map_allCases(data):
        data = np.hstack([v for _, v in data[0].items()])
        df = pd.DataFrame.from_records(data)
        return df.to_csv(line_terminator='\n', index=False)

    def map_casesByAge(data):
        data = data[0]['ageData']
        df = pd.DataFrame.from_records(data)
        return df.to_csv(line_terminator='\n', index=False)

    def map_casesByCounty(data):
        data = data[0]['cases']
        df = pd.DataFrame.from_records(data)
        return df.to_csv(line_terminator='\n', index=False)

    def map_casesByMunicipality(data):
        data = data[0]['cases']
        df = pd.DataFrame.from_records(data)
        return df.to_csv(line_terminator='\n', index=False)

    def map_timeseriesNew(data):
        data = data[0]['timeseries']['new']
        confimed = pd.DataFrame([(d, c) for d, c in data['confirmed'].items()], columns=['date', 'confirmed'])
        death = pd.DataFrame([(d, c) for d, c in data['dead'].items()], columns=['date', 'death'])
        return pd.merge(confimed, death).to_csv(line_terminator='\n', index=False)

    def map_timeseriesTotal(data):
        data = data[0]['timeseries']['total']
        confimed = pd.DataFrame([(d, c) for d, c in data['confirmed'].items()], columns=['date', 'confirmed'])
        death = pd.DataFrame([(d, c) for d, c in data['dead'].items()], columns=['date', 'death'])
        return pd.merge(confimed, death).to_csv(line_terminator='\n', index=False)

    maps = {k.split('_')[-1]: v for k, v in locals().items() if k.startswith('map_')}
    return maps[name] if name in maps else lambda x: ''
