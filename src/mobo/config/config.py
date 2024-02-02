import os
import requests
import tiktoken

class MoboConfig:
    def __init__(
        self,
        model,
        discord_token,
        open_ai_key,
        personality=None,
        personality_url=None,
        personality_tokens=0, #placeholder for the number of tokens in the personality, updated later on
        max_history_length=30,
        max_bot_responses=5,
        max_tokens_context=8192, #context window size, 8192 is the max for GPT-4, see: https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
        max_new_tokens=490, #helps prevent discord from needing to split the message into multiple messages
        is_llama=False, #if you're using a llama model, a different tokenizer is required  
        log_level="INFO",
    ):
        self.model = model
        self.max_history_length = int(max_history_length)
        self.max_bot_responses = int(max_bot_responses)
        self.discord_token = discord_token
        self.open_ai_key = open_ai_key
        self.personality_url = personality_url
        self.log_level = log_level
        self.max_tokens_context = int(max_tokens_context)
        self.max_new_tokens = int(max_new_tokens)
        self.is_llama = is_llama

        if personality:
          self.personality = personality

        else:
          self.personality = self.personality_from_url()

        if self.personality is None:
            raise Exception("Personality is required. The bot needs one too.")
        else:
           self.personality_tokens = len(tiktoken.encoding_for_model(model).encode(
              str([{"role": "system", "content": self.personality}])))

    def personality_from_url(self):
      response = requests.get(self.personality_url)
      if response.status_code == 200:
          return response.text
      else:
          raise Exception("Failed to load personality")
      

    @classmethod
    def from_env(cls):
        model = os.environ.get("MOBO_MODEL", "gpt-4")
        max_history_length = os.environ.get("MOBO_MAX_HISTORY_LENGTH", 30)
        max_bot_responses = os.environ.get("MOBO_MAX_BOT_RESPONSES", 5)
        personality_url = os.environ.get("MOBO_PERSONALITY_URL")
        discord_token = os.environ.get("DISCORD_API_KEY")
        open_ai_key = os.environ.get("OPENAI_API_KEY")
        log_level = os.environ.get("MOBO_LOG_LEVEL", "INFO")
        max_tokens_context = os.environ.get("MOBO_MAX_TOKENS_CONTEXT", 8192)
        personality_tokens = os.environ.get("MOBO_PERSONALITY_TOKENS", 0)
        max_new_tokens = os.environ.get("MOBO_MAX_NEW_TOKENS", 490)
        is_llama = os.environ.get("MOBO_IS_LLAMA", False)

        return cls(
            model=model,
            max_history_length=max_history_length,
            max_bot_responses=max_bot_responses,
            personality_url=personality_url,
            discord_token=discord_token,
            open_ai_key=open_ai_key,
            log_level=log_level,
            max_tokens_context=max_tokens_context,
            personality_tokens=personality_tokens,
            max_new_tokens=max_new_tokens,
            is_llama=is_llama,
        )
