class user:
    def __init__(self, displayname: str):
        self.displayname = displayname

class message:
    def __init__(self, user: user, content: str):
        self.user = user
        self.content = content
        self.id = None

class channel:
    def __init__(self):
        self.users = []
        self.messages = []
    
    def log(self, message: message):
        message.id = len(self.messages)
        self.messages.append(message)
        return message
    
    def log_raw(self, content: str):
        msg = message(None, content)
        self.messages.append(msg)
        return msg

'''
novial = user("novial")
general_chat = channel()

msg = message(novial, "Hello World")
general_chat.log(msg)

for message in general_chat.messages:
    print(f"({message.user.displayname}) {message.content}")
'''