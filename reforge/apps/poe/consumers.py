import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class PoeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(self.scope)
        await self.channel_layer.group_add(
            'poe_service',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'poe_service',
            self.channel_name
        )
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        print(text_data_json)

        if text_data_json.get('subscribe'):
            print('subscribe', text_data_json['subscribe'])
            await self.channel_layer.group_add(
                text_data_json['subscribe'],
                self.channel_name
            )

            # Send message to room group
            # await self.channel_layer.group_send(
            #     'poe_service',
            #     {
            #         'type': 'chat_message',
            #         'message': 'subscribed channel %s' % text_data_json['subscribe']
            #     }
            # )
            await self.send(text_data=json.dumps({
                'message': 'subscribed channel %s' % text_data_json['subscribe']
            }))

        if text_data_json.get('unsubscribe'):
            await self.channel_layer.group_discard(
                text_data_json['unsubscribe'],
                self.channel_name
            )

            # Send message to room group
            # await self.channel_layer.group_send(
            #     'poe_service',
            #     {
            #         'type': 'chat_message',
            #         'message': 'unsubscribed channel %s' % text_data_json['unsubscribe']
            #     }
            # )
            await self.send(text_data=json.dumps({
                'message': 'unsubscribed channel %s' % text_data_json['unsubscribe']
            }))

        # message = text_data_json['message']

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    # Receive message from room group
    async def service_update(self, event):
        service_id = event['service_id']
        pk = event['id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'service_update',
            'service_id': service_id,
            'id': pk
        }))

    async def vouch_update(self, event):
        print(event)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'vouch_update',
            'profile': event['profile']
        }))
