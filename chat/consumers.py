from channels import Group
from channels.sessions import channel_session
from .models import Room
import json

@channel_session
def ws_connect(message):
    try:
        print(message['path'])
        strList=message['path'].strip('/').split('/')
        prefix=strList[0]
        label=strList[1]

        if prefix != 'chat':
            return
        room=Room.objects.get(label=label)
    except(ValueError, Room.DoesNotExist):
        return

    Group('chat-'+label, channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session["room"]=room.label


@channel_session
def ws_receive(message):
    try:
        label=message.channel_session["room"]
        print("ws_receive : ")
        print(type(label))
        print(label)

        room=Room.objects.get(label=label)
    except(KeyError, Room.DoesNotExist):
        return

    try:
        data=json.loads(message['text'])
    except(ValueError):
        return

    if(set(data.keys()) != set(('handle', 'message'))):
        return

    if(data):
        m=room.messages.create(**data)
        Group('chat-'+label, channel_layer=message.channel_layer).send({'text':json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label=message.channel_session['room']
        room=Room.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except(KeyError, Room.DoesNotExist):
        return

