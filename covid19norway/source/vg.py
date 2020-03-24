from covid19norway.rawdata import download
from json import dumps
import pandas as pd
import numpy as np


SOURCE_MAP = {
    # 'allCases': 'https://www.vg.no/spesial/2020/corona-viruset/data/norway-allCases/',
    'casesByCounty': 'https://redutv-api.vg.no/corona/v1/sheets/norway-table-overview/?region=county',
    'casesByMunicipality': 'https://redutv-api.vg.no/corona/v1/sheets/norway-table-overview/?region=municipality',
    # 'casesByAge': 'https://redutv-api.vg.no/corona/v1/sheets/norway-age-data',
    'norwayData': 'https://redutv-api.vg.no/corona/v1/sheets/norway-region-data/',
    'tested': 'https://redutv-api.vg.no/corona/v1/sheets/fhi/tested',
    'hospitalsData': 'https://redutv-api.vg.no/corona/v1/areas/country/reports?include=hospitals',
    'ages': 'https://redutv-api.vg.no/corona/v1/sheets/fhi/age'
}


def __raw_data():
    return {k: download(v) for k, v in SOURCE_MAP.items()}


def json():
    return {k: dumps(v, indent=2) for k, v in __raw_data().items()}


def csv():
    data = __raw_data()

    data['timeseriesNew'] = data['norwayData']
    data['timeseriesTotal'] = data['norwayData']
    data['allCases'] = data['norwayData']
    data.pop('norwayData')

    data['hospitalsTimeseriesTotal'] = data['hospitalsData']
    data['hospitalsLatest'] = data['hospitalsData']
    data.pop('hospitalsData')

    return {k: __csv_mapper(k)(v) for k, v in data.items()}


def __csv_mapper(name: str):

    def map_allCases(data):
        data = data[0]['casesList']
        data = np.hstack([v for _, v in data.items()])
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

    def map_hospitalsTimeseriesTotal(data):
        data = data[0]['hospitals']['timeseries']['total']
        df = pd.DataFrame.from_records(data)
        return df.to_csv(line_terminator='\n', index=False)

    def map_hospitalsLatest(data):
        data = data[0]['hospitals']['hospitals']

        def apply(x):
            latest = x.pop('latest')
            return dict(x, **latest)

        data = [apply(v) for v in data]
        df = pd.DataFrame.from_records(data)
        return df.to_csv(line_terminator='\n', index=False)

    def map_tested(data):
        data = data[0]['timeseries']

        def apply(x):
            updated = x.pop('updated')
            return dict(x, **updated)

        data = [apply(v) for v in data]
        df = pd.DataFrame.from_records(data)
        return df.to_csv(line_terminator='\n', index=False)

    def map_ages(data):
        data = data[0]['timeseries']

        def apply(x):
            bins = x.pop('bins')
            return dict(x, **bins)

        data = [apply(v) for v in data]
        df = pd.DataFrame.from_records(data)
        return df.to_csv(line_terminator='\n', index=False)

    maps = {k.split('_')[-1]: v for k, v in locals().items() if k.startswith('map_')}

    def map_data(name):
        def mapper(value):
            mapper_func = maps[name]
            try:
                return mapper_func(value)
            except Exception as e:
                return str(e)
        return mapper

    return map_data(name) if name in maps else lambda x: ''
