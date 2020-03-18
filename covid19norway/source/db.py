from covid19norway.rawdata import download
from json import dumps
import pandas as pd


def __raw_data():
    api_url = 'https://www.dagbladet.no/app/crowdsource-corona-api/api/v1/municipality-stats'
    return download(api_url)[0]


def json():
    return {
        'crowdsource': dumps(__raw_data(), indent=2)
    }


def csv():
    data = __raw_data()
    data = [v for _, v in data['municipalities'].items()]
    df = pd.DataFrame.from_records(data)
    return {
        'crowdsource': df.to_csv(line_terminator='\n', index=False)
    }
