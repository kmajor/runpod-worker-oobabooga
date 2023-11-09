MODEL_SCHEMA = {
    'action': {
        'type': str,
        'required': True,
        'constraints': lambda action: action in [
            'load',
            'unload',
            'list',
            'info'
        ]
    },
    'model_name': {
        'type': str,
        'required': False,
        'default': 'TheBloke/Pygmalion-2-13B-GPTQ'
    },
    'args': {
        'type': dict,
        'required': False,
        'default': {}
    }
}
