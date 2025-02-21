import logging
from datetime import datetime
from openai import OpenAI
from .base_handler import BaseHandler
import tiktoken

_log = logging.getLogger()
_log.setLevel(logging.INFO)

class Message:
    def __init__(self, role, content, name=None, is_bot=False):
        self.role = role
        self.content = content
        self.name = name
        self.is_bot = is_bot

    def to_dict(self):
        return {
            attr: getattr(self, attr)
            for attr in ["role", "content", "name"]
            if getattr(self, attr) is not None
        }


class ChannelHistoryManager:
    def __init__(self):
        self.history = {}

    def add_message(self, channel_id, message):
        if channel_id not in self.history:
            self.history[channel_id] = []
        self.history[channel_id].append(message)

    def get_messages(self, channel_id):
        return self.history.get(channel_id, [])

    def get_messages_dict(self, channel_id):
        return [message.to_dict() for message in self.get_messages(channel_id)]

    def prune_messages(self, channel_id, number_of_messages, maxtokens, ptokens, model, is_llama):
        available_context = maxtokens - ptokens
        #print(f"Available Context: {available_context}")
        keep_messages,total_tokens = self.max_tokenized_messages(channel_id, model, available_context, is_llama)
        if channel_id in self.history:
            self.history[channel_id] = self.history[channel_id][-keep_messages:]
            #print(keep_messages)
            #print(total_tokens)

    def message_count(self, channel_id):
        response_count = 0
        if channel_id in self.history:
            response_count = len(self.history[channel_id])
        return response_count

    def bot_responses(self, channel_id):
        """
        Counts the number of bot messages in the history for a given channel_id.
        """
        response_count = 0
        if channel_id in self.history:
            response_count = sum(
                1 for message in self.history[channel_id] if message.is_bot
            )
        return response_count

    def max_tokenized_messages(self, channel_id, model, available_context, is_llama):
        tokenizer = tiktoken.encoding_for_model(model) #link this to the bot config somehow later
        total_tokens = 0
        keep_messages = 0
        if channel_id in self.history:
            for message in reversed(self.history[channel_id]):
                #print(message.to_dict())
                tokens = tokenizer.encode(str(message.to_dict()))
                if is_llama:
                    total_tokens += int(len(tokens)*1.2) #increase it by a flat % for llama models. I'm lazy and would rather count high than go over and the model breaks.
                else:
                    total_tokens += len(tokens)
                
                if total_tokens > available_context:
                    total_tokens -= len(tokens)
                    break
                keep_messages += 1
        return keep_messages, total_tokens


class ChatMessageHandler(BaseHandler):
    def __init__(self) -> None:
        super().__init__()
        self.open_ai_client = OpenAI()
        self.history = ChannelHistoryManager()

    async def handle(self, message, bot):
        channel_id = str(message.channel.id)
        prompt_tokens = 0

        if not message.author.bot or (
            message.author.bot
            and self.history.bot_responses(channel_id) <= bot.config.max_bot_responses
        ):
            self.history.add_message(
                channel_id,
                Message(
                    role="user", content=message.content, is_bot=message.author.bot
                ),
            )

            completion = self.open_ai_client.chat.completions.create(
                model=bot.config.model,
                messages=[{"role": "system", "content": bot.config.personality}]
                + self.history.get_messages_dict(channel_id),
                max_tokens=490,
            )

            bot_response = completion.choices[0].message.content
            chunks  = [bot_response[i:i+1900] for i in range(0, len(bot_response), 1900)]
            for chunk in chunks:
                await message.reply(chunk)

            self.history.add_message(
                channel_id,
                Message(role="assistant", content=bot_response),
            )

        self.history.prune_messages(channel_id, 
                                    bot.config.max_history_length, 
                                    bot.config.max_tokens_context,
                                    bot.config.personality_tokens,
                                    bot.config.model,
                                    bot.config.is_llama)
