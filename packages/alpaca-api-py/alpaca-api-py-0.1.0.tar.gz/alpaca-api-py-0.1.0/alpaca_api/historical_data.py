import time
import pandas as pd
import requests
import pytz


class AlpacaBadRequestException(Exception):
    pass


class AlpacaForbiddenException(Exception):
    pass


class AlpacaPageNotFoundException(Exception):
    pass


class AlpacaTooManyRequestsException(Exception):
    pass


class AlpacaServerErrorException(Exception):
    pass


class AlpacaNoDataException(Exception):
    pass


def validate_response(response):
    if response.status_code == 400:
        raise AlpacaBadRequestException
    elif response.status_code == 404:
        raise AlpacaForbiddenException
    elif response.status_code == 404:
        raise AlpacaPageNotFoundException
    elif response.status_code == 429:
        raise AlpacaTooManyRequestsException
    elif response.status_code >= 500:
        raise AlpacaServerErrorException


def strip_timezone(timestamp):
    return timestamp.split('+')[0]


def convert_to_aware_time(timestamp):
    tz = pytz.timezone('US/Eastern')
    return timestamp.astimezone(tz)


def fill_zero_values(df):
    for i in range(0, len(df.index)):
        if i != 0:
            if df['ask_price'].iloc[i] == 0:
                df.loc[i, 'ask_price'] = df['ask_price'].iloc[i-1]
            if df['bid_price'].iloc[i] == 0:
                df.loc[i, 'bid_price'] = df['bid_price'].iloc[i-1]

            if df['ask_size'].iloc[i] == 0:
                df.loc[i, 'ask_size'] = df['ask_size'].iloc[i-1]
            if df['bid_size'].iloc[i] == 0:
                df.loc[i, 'bid_size'] = df['bid_size'].iloc[i-1]
        else:
            if df['ask_price'].iloc[i] == 0:
                df.loc[i, 'ask_price'] = df['bid_price'].iloc[i]
            if df['bid_price'].iloc[i] == 0:
                df.loc[i, 'bid_price'] = df['ask_price'].iloc[i]

            if df['ask_size'].iloc[i] == 0:
                df.loc[i, 'ask_size'] = df['bid_size'].iloc[i-1]
            if df['bid_size'].iloc[i] == 0:
                df.loc[i, 'bid_size'] = df['ask_size'].iloc[i-1]
    return df


class AlpacaHistoricalData:
    def __init__(self, base_url, key_id, secret_key, use_proxy=False):
        self.base_url = base_url
        self.key_id = key_id
        self.secret_key = secret_key
        self.use_proxy = use_proxy

    def get_headers(self):
        """

        :return:
        """
        return {
            'APCA-API-KEY-ID': self.key_id,
            'APCA-API-SECRET-KEY': self.secret_key
        }

    def get_historical_quotes(self, symbol, start, end, feed='iex', limit=10000, is_test=False, insert_function=None):
        """
        :return:
        """
        params = {
            'start': start.isoformat(),
            'end': end.isoformat(),
            'feed': feed,
            'limit': limit
        }

        is_end = False
        results = pd.DataFrame()
        page_token = None
        while not is_end:
            if page_token:
                params['page_token'] = page_token
            url = "{url}/stocks/{symbol}/quotes".format(url=self.base_url, symbol=symbol)
            r = requests.get(url=url, headers=self.get_headers(), params=params)
            try:
                validate_response(r)
            except AlpacaTooManyRequestsException:
                print("To many requests, sleep for 3 seconds, then try again")
                time.sleep(3)
                continue

            data = r.json()
            df = pd.DataFrame.from_dict(data['quotes'])
            if df.empty:
                raise AlpacaNoDataException
            df.rename(
                columns={'t': 'timestamp', 'ax': 'ask_exchange', 'ap': 'ask_price', 'as': 'ask_size',
                         'bx': 'bid_exchange',
                         'bp': 'bid_price', 'bs': 'bid_size', 'c': 'conditions', 'z': 'tape'}, inplace=True)
            df['symbol'] = symbol
            df['timestamp'] = df['timestamp'].apply(strip_timezone)
            df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True)
            # convert the timezone because it is returning a RFC-3339 format which is in utc and needs to be in easter
            df['timestamp'] = df['timestamp'].apply(convert_to_aware_time)
            # back fill data so it doesn't have zeros in the bid, ask, and size
            df = fill_zero_values(df)
            results = results.append(df, ignore_index=True)
            page_token = data['next_page_token']
            if not page_token:
                is_end = True
            if insert_function:
                insert_function(df)
            if is_test:
                break

        results = results.sort_values(by='timestamp')

        return results
