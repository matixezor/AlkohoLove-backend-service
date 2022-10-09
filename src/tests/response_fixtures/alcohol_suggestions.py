SUGGESTION_ID_FIXTURE = "6299e8c94105e843197376fd"
NON_EXISTING_ID_FIXTURE = "629b7d3e25f64a0cdff6dbef"

SUGGESTION_POST_FIXTURE = {
    "barcode": "5902573006616",
    "kind": "wódka",
    "name": "Amundsen Vodka",
    "description": "Odważna, oryginalna i kreatywna."
}

SUGGESTION_POST_FIXTURE_NO_DESC = {
    "barcode": "5902573006616",
    "kind": "wódka",
    "name": "Amundsen Vodka"
}

SUGGESTION_SAME_USER_FIXTURE = {
    "barcode": "5900699104827",
    "kind": "piwo",
    "name": "Żywiec białe",
    "description": "Bardzo dobre na ciepłe dni."
}

SUGGESTION_POST_BARCODE_EXISTS_FIXTURE = {
    "barcode": "3800006901502",
    "kind": "wino",
    "name": "Witosha premium sweet red",
    "description": "Bardzo dobre tanie wino."
}

SUGGESTIONS_RESPONSE_FIXTURE = {
    "barcode": "5900699104827",
    "kind": "piwo",
    "name": "Żywiec białe",
    "descriptions": [
        "Białe piwo pszeniczne żywiec.",
        "Dobre piwo o aromacie kolendry."
    ],
    "id": "6299e8c94105e843197376fd",
    "user_ids": [
        "6288e2fdd5ab6070dde8db8c",
        "6288e2fdd5ab6070dde8db8b"
    ]
}

SUGGESTIONS_SEARCH_RESPONSE_FIXTURE = \
    {
        "suggestions": [
            {
                "barcode": "5900699104827",
                "kind": "piwo",
                "name": "Żywiec białe",
                "id": "6299e8c94105e843197376fd",
                "user_ids": [
                    "6288e2fdd5ab6070dde8db8c",
                    "6288e2fdd5ab6070dde8db8b"
                ],
                "descriptions": [
                    "Białe piwo pszeniczne żywiec.",
                    "Dobre piwo o aromacie kolendry."
                ]
            }
        ],
        "page_info": {
            "offset": 0,
            "limit": 10,
            "total": 1
        }
    }

ALL_SUGGESTIONS_RESPONSE_FIXTURE = \
    {'page_info': {'limit': 10, 'offset': 0, 'total': 3},
     'suggestions': [{'barcode': '5900699104827',
                      'descriptions': ['Białe piwo pszeniczne żywiec.',
                                       'Dobre piwo o aromacie kolendry.'],
                      'id': '6299e8c94105e843197376fd',
                      'kind': 'piwo',
                      'name': 'Żywiec białe',
                      'user_ids': ['6288e2fdd5ab6070dde8db8c',
                                   '6288e2fdd5ab6070dde8db8b']},
                     {'barcode': '3800006901502',
                      'descriptions': ['Czerwone wino deserowe słodkie.'],
                      'id': '6299eb5a894d907992ecbd7e',
                      'kind': 'wino',
                      'name': 'Witosha premium sweet red',
                      'user_ids': ['6288e2fdd5ab6070dde8db8d']},
                     {'barcode': '1111111111111',
                      'descriptions': ['Dobry likier ziołowy.', 'Bardzo dobry'],
                      'id': '6299eb5f31a05c42142ea55c',
                      'kind': 'likier',
                      'name': 'Jagermeister',
                      'user_ids': ['6288e2fdd5ab6070dde8db8c',
                                   '6288e2fdd5ab6070dde8db8d']}]}
