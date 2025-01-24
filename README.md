# Duck assistant

Duck assistant integrates [DuckDuckGo Chat API Python Client](https://github.com/tolgakurtuluss/duckgo-ai-chat-py) to fetch responses from GPT-4O-Mini, Claude-3-Haiku, Meta-Llama, and Mixtral.

The assistant features a web-based interface built with GTK and WebKit2. It can be run with prompts via command-line arguments, and it maintains a history of interactions in an HTML file. The HTML appearance and functionality can be configured and edited using the style.html and script.html files. When the window is open, it automatically refreshes and activates in response to a new prompt.

Please note that this is not a chat. In my use cases, when interacting with an AI, the conversation history can clutter new responses with irrelevant content and misunderstandingsl, so I prefer to handle each request independently.

## Setup Duck Assistant

Assuming you are at ~

```bash
git clone https://github.com/davidnsousa/duck-assistant
cd duck-assistant
python -m venv .
source bin/activate
pip install -r requiements.txt
```

## Usage

Assuming you have setup Duck Assistant at ~, use the following command:

```bash
source ~/duck-assistant/bin/activate
python ~/duck-assistant/duck-assistant.py --instance <model> --prompt <text>
```

Models available are `"gpt"`, `"llama"`, `"calude"`, `"mistral"`

### Cool way to use it

Often I use AI, for instance, for revising, elaborating, or explaing pieces of text or code. So I created a little bash script which pipes mouse text selections to my AI prompts automatically.

You need to have `dmenu` and `xclip` installed on your system for the following to work.

```bash
selection=$(xclip -o -selection primary)
prompt=$(echo -e "revise\nanswer\nelaborate\nexplain\ntranslate" | dmenu)
source ~/duck-assistant/bin/activate
python ~/duck-assistant/duck-assistant.py --instance "gpt" --prompt "$prompt : $selection"
```

This also allows for custom prompts and can be used without requiring mouse selections.