import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . import database
from channels.db import database_sync_to_async
connected_users = {}

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the user from the scope (this is optional, based on your authentication)
        self.user = self.scope.get("user")

        # Get the group name from the URL (e.g., `/ws/notifications/group_name/`)
        print(self.scope['url_route']['kwargs'].get('group_name'))
        self.group_name = self.scope['url_route']['kwargs'].get('group_name')

        if not self.group_name:
            # If group name is not provided, you can handle it (for example, by sending an error message)
            await self.close()
        # Join a group specific to the user
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        connected_users[self.group_name] = self.group_name

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        if self.group_name in connected_users.keys():
            del connected_users[self.group_name]

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        

        if self.group_name == 'superadmin':
        # Example: Broadcast a message to the user's group
            unreadby = []

            for user in data.get('users'):
                if user in connected_users.keys():
                    await self.channel_layer.group_send(
                        user,
                        {
                            "type": "send_notification",
                            "message": data,
                        }
                    )

                    # PUSH THE USER TO THE READ BY.
                else:
                     print('working')
                     unreadby.append(user)
                     await self.channel_layer.group_send(
                        self.group_name,
                        {
                            "type": "send_notification",
                            "message": user ,
                        }
                    )
            data['unreadby'] = unreadby
            try:
                del data['type']
            except:
                pass
            
            result = await database_sync_to_async(database.add_record)('notification', data)
            print(result)
                     
        else:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "send_notification",
                    "message": "No message allowed to send to superadmin.",
                }
            )

    async def send_notification(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))




class CallingAgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f"callingagent_{self.user_id}"

        # Join the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from the group
    async def send_notification(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))