from .base_handler import BaseHandler
from ..config import MoboConfig

class AdminCommandHandler(BaseHandler):
    async def handle(self, message, bot):
        if message.author.guild_permissions.administrator:
            response = ""
            parts = message.content.split(' ', 3)
            admin_command = parts[2] if len(parts) > 2 else None
            text = parts[3] if len(parts) > 3 else None

            command_handlers = {
                "help": self.handle_help,
                "get-personality": self.handle_get_personality,
                "set-personality": self.handle_set_personality,
                "set-personality-url": self.handle_set_personality_url,
                "reset-config": self.handle_reset_config,
                "get-model": self.handle_get_model,
                "set-model": self.handle_set_model,
                "get-personality-tokens": self.handle_get_personality_tokens,
                "max-new-tokens": self.handle_max_new_tokens,
                "max-tokens-context": self.handle_max_tokens_context,
                "set-llama-mode": self.handle_set_llama_mode,
            }

            handler = command_handlers.get(admin_command, self.handle_unknown_command)
            response = await handler(bot, text)
        else:
            response = "https://media.giphy.com/media/3eKdC7REvgOt2/giphy.gif"

        await message.reply(response)

    async def handle_help(self, bot, text):
        return "\n".join([
            "Available commands:",
            "`get-personality` - Returns the current personality text",
            "`set-personality <text>` - Changes the bot's personality text",
            "`set-personality-url <text>` - Changes the bot's personality url and loads it",
            "`reset-config` - Resets the bot's personality to default",
            "`get-model` - Returns the current model",
            "`set-model <text>` - Changes the bot's model",
            "`get-personality-tokens` - Returns the count of personality tokens",
            "`max-new-tokens [number]` - Sets the max number of tokens to generate",
            "`max-tokens-context [number]` - Changes context window size",
            "`set-llama-mode` - Changes the context tokenize for llama-based models",
        ])

    async def handle_get_personality(self, bot, text):
        return f"```\n{bot.config.personality}\n```"

    async def handle_set_personality_url(self, bot, text):
        if text:
            bot.config.personality_url = text
            bot.config.personality = self.personality_from_url()
            return "Personality set."
        else:
            return "Error: No personality url provided"

    async def handle_set_personality(self, bot, text):
        if text:
            bot.config.personality = text
            return "Personality set."
        else:
            return "Error: No personality text provided"

    async def handle_reset_config(self, bot, text):
        bot.config = MoboConfig.from_env()
        return "Config reset."

    async def handle_get_model(self, bot, text):
        return f"`{bot.config.model}`"

    async def handle_set_model(self, bot, text):
        if text:
            bot.config.model = text
            return f"Model set to {text}."
        else:
            return "Error: No model text provided"
    
    async def handle_get_personality_tokens(self, bot, text):
        return f"`{bot.config.personality_tokens}`"

    async def handle_max_new_tokens(self, bot, text):
        if text:
            bot.config.max_new_tokens = int(text)
            return f"Max new tokens set to {text}."
        else:
            return f"Current value: {bot.config.max_new_tokens}"
        
    async def handle_max_tokens_context(self, bot, text):
        if text:
            bot.config.max_tokens_context = int(text)
            return f"Max tokens context set to {text}."
        else:
            return f"Current value: {bot.config.max_tokens_context} \
            \nDefault for GPT-4 is 8192. \
            \n[Check this link](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) for other models."
        
    async def handle_set_llama_mode(self, bot, text):
        bot.config.is_llama = not bot.config.is_llama
        return f"Llama mode set to {bot.config.is_llama}."

    async def handle_unknown_command(self, bot, text):
        return "Unknown command. Use `help` for a list of available commands."
