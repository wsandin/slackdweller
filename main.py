import os
from slackclient import SlackClient
from pprint import pprint
from typing import List

slack_token = os.environ.get("SLACK_API_TOKEN")


class SlackAPIConversationsError(Exception):
    pass


class SlackApp:
    def __init__(self, name: str, token: str, channels: List[str]):
        self.name = name
        self.token = token
        self.channels = channels

        self.sc = SlackClient(token=self.token)

    def join_all_channels(self):
        """Join all channels supplied to object

       :return: Returns list of the joined channels
       :rtype: list
        """
        [
            self.sc.api_call("conversations.join", channel=self.get_channel_id(chan))
            for chan in self.channels
        ]

        return self.channels

    def get_channel_id(self, channel_name: str):
        """Resolve channel names to IDs used by the API

        :param channel_name: The channel name
        :type channel_name: str
        :return: Returns the channel ID
        :rtype: str
        """
        conv_list = self.sc.api_call(
            "conversations.list", exclude_archived=1, limit=1000
        )

        # Log if the there's more than 1000 elements or do some pagination

        for chan in conv_list.get("channels", {}):
            if chan.get("name", "") == channel_name:
                channel_id = chan.get("id", "")

        if not channel_id:
            raise SlackAPIConversationsError(
                f"{channel_name} not found in channels dict"
            )

        return channel_id

    def leave_all_channels(self):
        """Retrieve a list of channel membership, and leave

        :return: Returns a list of left conversations
        :rtype: list
        """
        left_channels = []

        conv_list = self.sc.api_call(
            "conversations.list", exclude_archived=1, limit=1000
        )

        for chan in conv_list.get("channels", {}):
            if chan.get("is_member") == True:
                self.sc.api_call("conversations.leave", channel=chan.get("id"))
                left_channels += [conv_list.get("name")]

        return left_channels
