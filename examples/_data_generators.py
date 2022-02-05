import pandas as pd
import datetime


def generate_user_interaction_dataframe():
    row = {
        'hit_type': 'page',
        'hit': 'page',
        'user_id': '24d5ad1e-c201-4f16-a0cb-c6d64077e3e4',
        'date': datetime.date(2021, 1, 1),
        'session_id': '351513136135',
        'page': 'lager/overview',
        'timestamp': 1642574537437,
        'product_codes': [35113, 76869],
        'store': 'MainStore',
        'country': 'Sweden'
    }
    df = pd.DataFrame([row for _ in range(365)])
    dates = [datetime.date(2021, 1, 1) + datetime.timedelta(days=x) for x in range(len(df))]
    df.loc[:, 'date'] = dates
    # Randomly "remove" some dates by replacing with already existing date
    df.loc[df.sample(5, random_state=42).index, 'date'] = datetime.date(2021, 1, 1)
    return df


def generate_orders_dataframe():
    row = {
        'user_id': '24d5ad1e-c201-4f16-a0cb-c6d64077e3e4',
        'timestamp': 1642574537437,
        'date': datetime.date(2021, 1, 1),
        'product_codes': [456, 654],
        'country': 'Sweden',
        'store': 'MainStore',
        'order_id': '31531512',
        'order_status': 'completed',
        'price': 351.31,
        'currency': 'EUR'
    }
    df = pd.DataFrame([row for _ in range(365)])
    dates = [datetime.date(2021, 1, 1) + datetime.timedelta(days=x) for x in range(len(df))]
    df.loc[:, 'date'] = dates
    # Randomly "remove" some dates by replacing with already existing date
    df.loc[df.sample(5, random_state=11).index, 'date'] = datetime.date(2021, 1, 1)
    return df


def generate_beer_reviews_dataframe():
    row = {
        'user_id': '24d5ad1e-c201-4f16-a0cb-c6d64077e3e4',
        'timestamp': 1642574537437,
        'date': datetime.date(2021, 1, 1),
        'product_code': 321,
        'product_name': 'Carlsmountain Silver',
        'product_category': 'Lager',
        'ratings': {
            'taste': 4,
            'design': 5
        },
        'is_guest': False
    }
    df = pd.DataFrame([row for _ in range(365)])
    dates = [datetime.date(2021, 1, 1) + datetime.timedelta(days=x) for x in range(len(df))]
    df.loc[:, 'date'] = dates
    # Randomly "remove" some dates by replacing with already existing date
    df.loc[df.sample(5, random_state=42).index, 'date'] = datetime.date(2021, 1, 1)
    return df


def generate_beer_info_dataframe():
    row = {
        'product_code': 321,
        'product_name': 'Carlsmountain Silver',
        'product_category': 'Lager',
        'country': 'Sweden',
        'description': 'Probably the west beer in the world',
        'profile': {
            'bitterness': 4,
            'sourness': 5
        },
        'alcohol_content': 5.4,
    }
    df = pd.DataFrame([row for _ in range(120)])
    return df
