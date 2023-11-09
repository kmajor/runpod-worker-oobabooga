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
        "input": {
            "api": {
                "method": "POST",
                "endpoint": "/chat"
            },
            "payload": {
            "name1": "JohnnyB",
            "name2": "Mio",
            "context":"Mio is a super slutty college student from Taiwan who works as a part time call girl. You're currently talking with her at a party.",
            "chat_instruct_command": "Continue the chat dialogue below. Write a single reply for Mio.",
            "your_name": "JohnnyB",
            "mode": "chat",
            "stopping_strings": [
                "\n<|system|>",
                "\n<|user|>",
                "\n<|model|>"
            ],
            "user_input": "Where are we and who are you?",
            "history": {
                "internal": [
                    [
                        "Hi Mio, youre so cute.",
                        "Thanks I know it!"
                    ],
                    [
                        "Where do you live?",
                        "In a taco shop."
                    ],
                    [
                        "Really?  That interesting, tell me more.",
                        "Well I love tacos, so it works out!"
                    ],
                    [
                        "Where are we and who are you?",
                        ""
                    ]
                ],
                "visible": [
                    [
                        "Hi Mio, youre so cute.",
                        "Thanks I know it!"
                    ],
                    [
                        "Where do you live?",
                        "In a taco shop."
                    ],
                    [
                        "Really?  That interesting, tell me more.",
                        "Well I love tacos, so it works out!"
                    ],
                    [
                        "Where are we and who are you?",
                        ""
                    ]
                ]
            }
        },
            "message_uid": "123456789"
        }
    }

    # Save the payload to a JSON file
    with open('test_input.json', 'w') as output_file:
        json.dump(heartbeatPayload, output_file)

    print('Payload saved to: test_input.json')
