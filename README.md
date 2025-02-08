# Duck assistant

Duck assistant is based on [DuckDuckGo Chat API Python Client](https://github.com/tolgakurtuluss/duckduckgo-ai-chat-py) to fetch responses from O3-Mini, GPT-4O-Mini, Claude-3-Haiku, Meta-Llama, and Mixtral.

The assistant features a web-based interface built with GTK and WebKit2. It can be run with prompts via command-line arguments, and it maintains a history of interactions in an HTML file. The HTML appearance and functionality can be configured and edited using the style.html and script.html files. When the window is open, it automatically refreshes and activates in response to a new prompt. A toolbar on the right allows you to navigate and search through previous interactions.

Please note that this is not a chat. In my experience with AI, conversation history can sometimes introduce irrelevant content and misunderstandings into new responses, so I prefer to handle each independently.

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

Activate the virtual python environment:

```bash
source bin/activate
```

Running the program without any arguments will display previous interactions. Running for the first time, will show the usage instructions instead.

```bash
python duck-assistant.py
```

Prompting:

```bash
python duck-assistant.py --instance <model> --prompt <text>
```

Where `<model>` can be any of the following `"o3"`, `"gpt"`, `"llama"`, `"calude"`, `"mistral"`. Default is `"gpt"`.

To clear all previous interactions simply delete the `history.html` file:

```bash
rm history.html
```

### Examples

Using the default `"gpt"` model:

```bash
python duck-assistant.py --prompt "Ohm's Law"
```

Using another model:

```bash
python duck-assistant.py --instance "llama" --prompt "Hello world in Python"
```

### Cool way to use it

Often I use AI for revising, elaborating, or explaing pieces of text or code. So I created a little bash script which pipes mouse text selections to my AI prompts automatically. This is particularly useful when triggered by a keyboard shortcut.

You need to have `dmenu` and `xclip` installed on your system for the following to work.

```bash
cd ~/duck-assistant
selection=$(xclip -o -selection primary)
prompt=$(echo -e "revise\nanswer\nelaborate\nexplain\ntranslate" | dmenu)
if [[ -n "$prompt" ]]; then
    source bin/activate
    python duck-assistant.py --instance "gpt" --prompt "$prompt : $selection" &
    xclip -selection primary /dev/null
fi
```

This also allows for custom prompts and can be used without requiring mouse selections.