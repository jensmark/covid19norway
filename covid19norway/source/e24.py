import pandas as pd
from datetime import datetime
from urllib.parse import quote

URL_BASE = 'https://e24.no/spesial/2020/coronaviruset/data/'
LISTS = [
    'Advokat og revisjon',
    'Andre',
    'Bil',
    'Bygg og anlegg',
    'Finansiering og forsikring',
    'Industri',
    'Informasjon og kommunikasjon',
    'Kultur, underholdning og fritid',
    'Olje og gass',
    'Servering, kantine og kontor',
    'Transport',
    'Trening',
    'Varehandel'
]


def __raw_data():
    def make_df(l):
        filename = quote(f'LISTER - til publisering - {l}')
        url = f'{URL_BASE}{filename}.csv'
        df = pd.read_csv(url)
        df['date'] = datetime.utcnow().isoformat()
        return df

    df = pd.concat([make_df(x) for x in LISTS])
    return df


def json():
    return {
        'permitteringer': __raw_data().to_json(orient='table', index=False)
    }


def csv():
    return {
        'permitteringer': __raw_data().to_csv(line_terminator='\n', index=False)
    }
