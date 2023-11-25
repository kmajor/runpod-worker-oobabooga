API_SCHEMA = {
    'method': {
        'type': str,
        'required': True,
        'constraints': lambda method: method in [
            'GET',
            'POST'
        ]
     },
    'endpoint': {
        'type': str,
        'required': True,
        'constraints': lambda endpoint: endpoint in [
            'chat/completions',
            'models'
        ]
    }
}
