# Duck assistant

Duck assistant integrates [DuckDuckGo Chat API Python Client](https://github.com/tolgakurtuluss/duckduckgo-ai-chat-py) to fetch responses from GPT-4O-Mini, Claude-3-Haiku, Meta-Llama, and Mixtral.

The assistant features a web-based interface built with GTK and WebKit2. It can be run with prompts via command-line arguments, and it maintains a history of interactions in an HTML file. The HTML appearance and functionality can be configured and edited using the style.html and script.html files. When the window is open, it automatically refreshes and activates in response to a new prompt.

Please note that this is not a chat. In my experience with AI, the conversation history can pollute new responses with irrelevant content and misunderstandings, so I prefer to handle each request independently.

## Setup Duck Assistant

Make sure `WebKit2` is installed on your system.

```bash
git clone https://github.com/davidnsousa/duck-assistant
cd duck-assistant
python -m venv .
source bin/activate
pip install -r requirements.txt
```

## Usage

Navigate to the `duck-assistant` directory and run:

```bash
source bin/activate
python duck-assistant.py --instance <model> --prompt <text>
```

Where `<model>` can be any of the following `"gpt"`, `"llama"`, `"calude"`, `"mistral"`.

To view the history of previous requests run:

```bash
source bin/activate
python duck-assistant.py
```

### Cool way to use it

Often I use AI for revising, elaborating, or explaing pieces of text or code. So I created a little bash script which pipes mouse text selections to my AI prompts automatically.

You need to have `dmenu` and `xclip` installed on your system for the following to work.

```bash
cd ~/duck-assistant
selection=$(xclip -o -selection primary)
prompt=$(echo -e "revise\nanswer\nelaborate\nexplain\ntranslate" | dmenu)
source bin/activate
python duck-assistant.py --instance "gpt" --prompt "$prompt : $selection"
xclip -selection primary /dev/null
```

This also allows for custom prompts and can be used without requiring mouse selections.