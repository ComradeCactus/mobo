# mobo

MOckBOt: A Discord/ChatGPT bot that can take on whatever personality you write.

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
```shell
git clone https://github.com/ComradeCactus/mobo.git
cd mobo
docker build -t mobo:ccdev .
docker run -d \
-e OPENAI_API_KEY="<YOUR OPENAI API KEY>" \
-e DISCORD_API_KEY="<YOUR DISCORD API KEY>" \
-e MOBO_PERSONALITY_URL="https://gist.githubusercontent.com/cjonesy/3876ce2b74d70762a84cf651acce615a/raw/7d5cf0d1d1e68f2291a3a1468ff210771842ebed/clyde" \
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
The last line will run python.

## Environment Variables/Configuration
Required Variables:
```shell
MOBO_PERSONALITY_URL=""
DISCORD_API_KEY=""
OPENAI_API_KEY=""
```
Optional variables:
```shell
MOBO_MODEL="gpt-4"
MOBO_MAX_HISTORY_LENGTH="30" 
MOBO_MAX_BOT_RESPONSES="5" 
MOBO_LOG_LEVEL="INFO"
MOBO_MAX_TOKENS_CONTEXT="8192"
MOBO_MAX_NEW_TOKENS="490" 
MOBO_IS_LLAMA=False 
```
The application also supports the openai-python environment variables, such as **OPENAI_BASE_URL**, if you wanted to use it with something like ooba's text-generation-ui.

## Bot Commands

In order to invoke admin commands, you need to @ the bot first.

`!admin help` - Show these options on a running bot  
`!admin get-personality` - Returns the current personality text  
`!admin set-personality <text>` - Changes the bot's personality text  
`!admin set-personality-url <text>` - Changes the bot's personality url and loads it  
`!admin reset-config` - Resets the bot's personality to default  
`!admin get-model` - Returns the current model  
`!admin set-model <text>` - Changes the bot's model  
`!admin get-personality-tokens` - Returns the count of personality tokens  
`!admin max-new-tokens [number]` - Sets the max number of tokens to generate  
`!admin max-tokens-context [number]` - Changes context window size  
`!admin set-llama-mode` - Changes the context tokenize for llama-based models  