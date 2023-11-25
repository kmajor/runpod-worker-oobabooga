CHAT_COMPLETIONS_SCHEMA = {
    'mode': {
        'type': str,
        'required': True,
        'constraints': lambda mode: mode == 'chat'
    },
    'messages': {
        'type': list,
        'required': True,
        'constraints': lambda messages: all(
            'role' in message and 'content' in message and
            message['role'] in ['system', 'user', 'assistant'] and
            isinstance(message['content'], str)
            for message in messages
        )
    }
}