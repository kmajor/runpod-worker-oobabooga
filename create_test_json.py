#!/usr/bin/env python3
import json

if __name__ == '__main__':
    # Create the payload dictionary

    heartbeatPayload = {
        "input": {
            "heartbeat": True
        } 
    }

    payload = {
        "message_uid": "123456",
        "webhook": "https://live-enormous-trout.ngrok-free.app/api/v1/update_pending_chat_request",
        "input": {
            "api": {
                "endpoint": "/chat/completions",
                "method": "POST"
            },
            "payload": {
                "mode": "chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a sexy chat bot."
                    },
                    {
                        "role": "user",
                        "content": "Holy shit you're so hot, I bet your pussy is yummy! Can I eat it?  How do you like it?"
                    }
                ]
            }
        }
}

    # Save the payload to a JSON file
    with open('test_input.json', 'w') as output_file:
        json.dump(heartbeatPayload, output_file)
        #json.dump(payload, output_file)

    print('Payload saved to: test_input.json')
