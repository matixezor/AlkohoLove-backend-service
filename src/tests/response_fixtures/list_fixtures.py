WISHLIST_FIXTURE = [
    {
        'name': 'Jameson',
        'kind': 'whisky',
        'type': 'blended',
        'alcohol_by_volume': 40.0,
        'description': 'Lorem ipsum',
        'color': 'bursztyn',
        'manufacturer': 'Irish Distillers',
        'country': 'Irlandia',
        'region': 'Cork',
        'food': ['czekoladowy mus'],
        'finish': ['gładki', 'słodki', 'pikantny'],
        'aroma': ['kwiaty', 'owoce', 'nuty korzenne', 'drewno'],
        'taste': ['nuty korzenne', 'orzechy', 'wanilia', 'słodkie sherry', 'łagodny'],
        'barcode': ['5011007003234', '5011007015534', '5011007003005'],
        'keywords': ['czteroletnia', 'irlandzka', 'irlandzkie', 'blend'],
        'id': '6288e32dd5ab6070dde8db8a',
        'avg_rating': 5.0,
        'rate_count': 1,
        'rate_value': 5,
        'additional_properties': [{
            'name': 'age',
            'display_name': 'wiek',
            'value': 4
        }]
    },
    {
        'name': 'Jameson Caskmates Stout Edition',
        'kind': 'whisky',
        'type': 'blended',
        'alcohol_by_volume': 40.0,
        'description': 'Lorem ipsum',
        'color': 'karmel',
        'manufacturer': 'Irish Distillers',
        'country': 'Irlandia',
        'region': 'Cork',
        'food': ['ser'],
        'finish': ['długi', 'słodki', 'mleczna czekolada', 'karmel'],
        'aroma': ['owoce', 'jabłko', 'gruszka', 'nuty korzenne', 'orzechy', 'skórka limonki'],
        'taste': ['mleczna czekolada', 'chmiel', 'kakao', 'marcepan'],
        'barcode': ['5011007025427'],
        'keywords': ['czteroletnia', 'irlandzka', 'irlandzkie', 'blend', 'piwo'],
        'id': '6288e32dd5ab6070dde8db8b',
        'avg_rating': 3.0,
        'rate_count': 2,
        'rate_value': 6,
        'additional_properties': [{
            'name': 'age',
            'display_name': 'wiek',
            'value': 4
        }]
    }
]

FAVOURITES_FIXTURE = [
    {
        "id": '6288e32dd5ab6070dde8db8c',
        "barcode": ['7312040017072'],
        "kind": 'wódka',
        "name": 'Absolut Vodka',
        "type": 'czysta',
        "description": 'Lorem ipsum',
        "alcohol_by_volume": 40.0,
        "color": 'bezbarwny',
        "country": 'Szwecja',
        "region": 'Ahus',
        "manufacturer": 'The Absolut Company',
        "food": [],
        "taste": [],
        "aroma": [],
        "finish": [],
        "rate_count": 0,
        "rate_value": 0,
        "avg_rating": 0.0,
        "keywords": ['szwedzka'],
        'additional_properties': []
    },
    {
        "id": '6288e32dd5ab6070dde8db8e',
        "barcode": ['5900595008427'],
        "kind": 'likier',
        "name": 'Kupnik Pigwa',
        "type": 'owocowy',
        "description": 'Lorem ipsum',
        "alcohol_by_volume": 30.0,
        "color": 'pomarańczowy',
        "country": 'Polska',
        "region": None,
        "manufacturer": 'Sobieski Sp. z o.o.',
        "food": [],
        "taste": ['pigwa'],
        "aroma": [],
        "finish": [],
        "rate_count": 0,
        "rate_value": 0,
        "avg_rating": 0.0,
        "keywords": ['wódka', 'pigwowa', 'pigwowy'],
        'additional_properties': []
    }
]

SEARCH_HISTORY_FIXTURE = [
    {
        'alcohol':
            {
                'additional_properties': [{
                    'name': 'age',
                    'display_name': 'wiek',
                    'value': 4
                }],
                'alcohol_by_volume': 40.0,
                'aroma': ['kwiaty', 'owoce', 'nuty korzenne', 'drewno'],
                'avg_rating': 5.0,
                'barcode': ['5011007003234', '5011007015534', '5011007003005'],
                'color': 'bursztyn',
                'country': 'Irlandia',
                'description': 'Lorem ipsum',
                'finish': ['gładki', 'słodki', 'pikantny'],
                'food': ['czekoladowy mus'],
                'id': '6288e32dd5ab6070dde8db8a',
                'keywords': ['czteroletnia', 'irlandzka', 'irlandzkie', 'blend'],
                'kind': 'whisky',
                'manufacturer': 'Irish Distillers',
                'name': 'Jameson',
                'rate_count': 1,
                'rate_value': 5,
                'region': 'Cork',
                'taste': ['nuty korzenne',
                          'orzechy',
                          'wanilia',
                          'słodkie sherry',
                          'łagodny'],
                'type': 'blended',

            },
        'date': '2022-04-25T19:13:25+00:00'
    },
    {
        'alcohol':
            {
                'additional_properties': [{
                    'name': 'age',
                    'display_name': 'wiek',
                    'value': 4
                }],
                'alcohol_by_volume': 40.0,
                'aroma': ['owoce',
                          'jabłko',
                          'gruszka',
                          'nuty korzenne',
                          'orzechy',
                          'skórka limonki'],
                'avg_rating': 3.0,
                'barcode': ['5011007025427'],
                'color': 'karmel',
                'country': 'Irlandia',
                'description': 'Lorem ipsum',
                'finish': ['długi', 'słodki', 'mleczna czekolada', 'karmel'],
                'food': ['ser'],
                'id': '6288e32dd5ab6070dde8db8b',
                'keywords': ['czteroletnia',
                             'irlandzka',
                             'irlandzkie',
                             'blend',
                             'piwo'],
                'kind': 'whisky',
                'manufacturer': 'Irish Distillers',
                'name': 'Jameson Caskmates Stout Edition',
                'rate_count': 2,
                'rate_value': 6,
                'region': 'Cork',
                'taste': ['mleczna czekolada', 'chmiel', 'kakao', 'marcepan'],
                'type': 'blended'
            },
        'date': '2022-07-21T19:13:25+00:00'
    }
]
