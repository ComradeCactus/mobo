# mobo

MOckBOt: A Discord/ChatGPT bot that can take on whatever personality you write.

Works with OpenAI's APIs, or Oobabooga's [text-generation-webui](https://github.com/oobabooga/text-generation-webui)

Running the original, using OpenAI:

```shell
source .env
docker run \
  -d \
  -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
  -e DISCORD_API_KEY="${DISCORD_API_KEY}" \
  -e MOBO_PERSONALITY_URL=https://gist.githubusercontent.com/cjonesy/3876ce2b74d70762a84cf651acce615a/raw/7d5cf0d1d1e68f2291a3a1468ff210771842ebed/clyde \
  ghcr.io/cjonesy/mobo:main
```

## Building this version for Docker
Read through the other environment variables below before running `docker run` in order to set your configuration.
```shell
git clone https://github.com/ComradeCactus/mobo.git
cd mobo
docker build -t mobo:ccdev .
docker run -d \
-e OPENAI_API_KEY="<YOUR OPENAI API KEY>" \
-e DISCORD_API_KEY="<YOUR DISCORD API KEY>" \
-e MOBO_PERSONALITY_URL="https://gist.githubusercontent.com/cjonesy/3876ce2b74d70762a84cf651acce615a/raw/7d5cf0d1d1e68f2291a3a1468ff210771842ebed/clyde" \
-e PUT_OTHER_ENV_VARIABLES="here" \
mobo:ccdev
```

## Running without Docker
Great for developing! Or, if you don't vibe with Docker.
```shell
git clone https://github.com/ComradeCactus/mobo.git
python -m venv ./mobo/venv
souce ./mobo/venv/bin/activate
pip install discord.py==2.3.2 openai==1.3.5 requests==2.28.1 tiktoken==0.5.2
cd ./mobo/src
OPENAI_API_KEY="<YOUR OPENAI API KEY>" DISCORD_API_KEY="<YOUR DISCORD API KEY>" MOBO_PERSONALITY_URL="https://gist.githubusercontent.com/cjonesy/3876ce2b74d70762a84cf651acce615a/raw/7d5cf0d1d1e68f2291a3a1468ff210771842ebed/clyde" python -m mobo
```
The last line will run python and the bot.  
Stick any extra variables you want in front of the `python -m mobo` command.

## Environment Variables/Configuration
### Required Variables

You should probably know how to get these.

`MOBO_PERSONALITY_URL=""`  
The personality URL that you want to load. Should be plaintext, no other markers.

`DISCORD_API_KEY=""`  
Create a Discord bot token: https://discord.com/developers/applications

`OPENAI_API_KEY=""`  
Get an OpenAI API key: https://platform.openai.com/docs/quickstart  
This variable is ignored by text-generation-webui.


### Optional variables:

`MOBO_MODEL="gpt-4"`  
Sets the OpenAI model to use. [Other models here.](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) Ignored by text-generation-webui. 

`MOBO_MAX_HISTORY_LENGTH="30"`   
Sets the number of messages to keep. Replaced by sliding context window.  

`MOBO_MAX_BOT_RESPONSES="5"`  
How many times this bot will respond to another bot. 

`MOBO_LOG_LEVEL="INFO"`  
Logging level.  

`MOBO_MAX_TOKENS_CONTEXT="8192"`  
The maximum context your model can handle before breaking. [Check this link for max context window sizes for your model if using OpenAI.](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo)  

`MOBO_MAX_NEW_TOKENS="490"`  
The number of new tokens the bot should generate. This should keep it from splitting messages in Discord.

`MOBO_IS_LLAMA=False`  
Only really useful if you're using text-generation-webui with a llama.cpp bot. Just adds 20% to the token counts internally because I'm lazy.

`OPENAI_BASE_URL="http://your.text-gen-webui.server:5000/v1"`  
Use this when connecting your bot to text-generation-webui. You'll need to set it up to use the OpenAI API module before this will work.

The bot also supports other openai-python environment variables.

## Bot Commands

In order to invoke admin commands, you need to @ the bot first.

`!admin help`  
Show these options on a running bot  

`!admin get-personality`  
Returns the current personality text  

`!admin set-personality <text>`  
Changes the bot's personality text  

`!admin set-personality-url <text>`  
Changes the bot's personality url and loads it  

`!admin reset-config`  
Resets the bot's personality to default  

`!admin get-model`  
Returns the current model  

`!admin set-model <text>`  
 Changes the bot's model. 

`!admin get-personality-tokens`  
Returns the count of tokens in the bot's personality that will count against your total context.

`!admin max-new-tokens [number]`  
Sets the max number of tokens to generate, shows the current value if nothing is provided

`!admin max-tokens-context [number]`  
Changes context window size, shows the current value if nothing is provided [Check this link for OpenAI.](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo)

`!admin set-llama-mode`  
Changes the context tokenizer counter for llama-based models  