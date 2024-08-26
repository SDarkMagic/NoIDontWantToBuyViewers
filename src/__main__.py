import os
import re
from twitchio import Client, Message

LINK_PATTERN = r'.*\.*{2,4}\/.*'

class ModClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = args[0]

    async def event_ready(self):
        channels = os.getenv('CHANNELS').split(',')
        await self.join_channels(channels)
        print('Successfully connected to channels!')

    async def event_message(self, msg: Message):
        #print(msg.content)
        if not msg.first:
            return
        msg_split = msg.content.split()
        for string in msg_split:
            if (re.search(LINK_PATTERN, string, re.IGNORECASE) != None):
                print(f'Matched potential link on first message from user {msg.author.name}; {string}')
                channel_user = await msg.channel.user()
                channel = self.create_user(channel_user.id, channel_user.name)
                if channel == None:
                    print(f'Error creating user object for channel: "{msg.channel.name}"')
                    return
                # if not self.is_mod(): return
                reason = f'Attempting to promote viewbots through the link: {string}'
                try:
                    await channel.ban_user(self.token, self.user_id, int(msg.author.id), reason)
                except:
                    print(f'Failed performing ban on user {msg.author.name} in channel {msg.channel.name}')
                return
        return



def main():
    token = os.getenv('OAUTH_TOKEN')
    secret = os.getenv('CLIENT_SECRET')
    client = ModClient(token, client_secret=secret)
    client.run()
    return

if __name__ == '__main__':
    main()