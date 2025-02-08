from datetime import datetime
import asyncio
import httpx
import json
import argparse
import markdown
import gi
import dbus
import dbus.service
import dbus.mainloop.glib
import os
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2, GLib

# AI REQUESTS

STATUS_URL = "https://duckduckgo.com/duckchat/v1/status"
CHAT_URL = "https://duckduckgo.com/duckchat/v1/chat"
STATUS_HEADERS = {"x-vqd-accept": "1"}

class Model:
    O3_MINI = "o3-mini"
    GPT_4O_MINI = "gpt-4o-mini"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    META_LLAMA = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    MISTRALAI = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def choose_model(input_string):
    model_mapping = {
        "o3": Model.O3_MINI,
        "gpt": Model.GPT_4O_MINI,
        "claude": Model.CLAUDE_3_HAIKU,
        "llama": Model.META_LLAMA,
        "mistral": Model.MISTRALAI
    }
    input_string = input_string.lower()
    return model_mapping.get(input_string, "Model not found")

class Chat:
    def __init__(self, vqd: str, model: str):
        self.old_vqd = vqd
        self.new_vqd = vqd
        self.model = model
        self.messages = []

    async def fetch(self, content: str) -> httpx.Response:
        self.messages.append({"content": content, "role": "user"})
        payload = {
            "model": self.model,
            "messages": self.messages,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CHAT_URL,
                headers={"x-vqd-4": self.new_vqd, "Content-Type": "application/json"},
                json=payload
            )
            if not response.is_success:
                raise Exception(f"{response.status_code}: Failed to send message. {response.text}")
            return response

    async def fetch_full(self, content: str) -> str:
        message = await self.fetch(content)
        full_message = await self.stream_events(message)
        self.old_vqd = self.new_vqd
        self.new_vqd = message.headers.get("x-vqd-4")
        self.messages.append({"content": full_message, "role": "assistant"})
        return full_message

    async def stream_events(self, message: httpx.Response):
        full_message = ""
        async for line in message.aiter_lines():
            if line:
                line = line[len("data: "):].strip()
                if line == "[DONE]":
                    break
                try:
                    json_data = json.loads(line)
                    if "message" in json_data:
                        full_message += json_data["message"]
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line}")
        return full_message

    def redo(self):
        self.new_vqd = self.old_vqd
        self.messages.pop()
        self.messages.pop()

async def init_chat(model: str) -> Chat:
    async with httpx.AsyncClient() as client:
        status = await client.get(STATUS_URL, headers=STATUS_HEADERS)
        vqd = status.headers.get("x-vqd-4")
        if not vqd:
            raise Exception(f"{status.status_code}: Failed to initialize chat. {status.text}")
        return Chat(vqd, model)

# WEBVIEW

SERVICE = "com.App"
SERVICE_PATH = "/com/App"

class refreshWebviewService(dbus.service.Object):
    def __init__(self, app):
        self.app = app
        bus_name = dbus.service.BusName(SERVICE, bus=dbus.SessionBus())
        super().__init__(bus_name, SERVICE_PATH)

    @dbus.service.method(SERVICE)
    def refresh_webview(self,content):
        self.app.refresh(content)

class CreateWebView:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("Assistant")
        self.window.set_default_size(1200, 1000)
        self.window.connect("destroy", Gtk.main_quit)
        self.window.set_position(Gtk.WindowPosition.CENTER)

        self.webview = WebKit2.WebView()
        self.window.add(self.webview)

    def refresh(self,content):
        self.webview.load_html(content)
        self.window.present() 

    def is_active(self):
        return self.window.get_property("active")


    def run(self,content):
        self.refresh(content)
        self.window.show_all()
        Gtk.main()

# ChatFetcher

class ChatFetcher:
    def __init__(self, instance):
        self.instance = instance
        self.chat_instance = None

    async def init_chat(self):
        self.chat_instance = await init_chat(self.instance)

    async def fetch_response(self, prompt):
        if self.chat_instance is None:
            await self.init_chat()
        
        responseMD = await self.chat_instance.fetch_full(prompt)
        responseHTML = markdown.markdown(responseMD.replace("\\", "\\\\"), extensions=['fenced_code'])
        return responseHTML

def build_main():
    with open("style.html", 'r', encoding='utf-8') as file:
        style = file.read()

    with open("script.html", 'r', encoding='utf-8') as file:
        script = file.read()

    if os.path.isfile("history.html"):
        with open("history.html", 'r', encoding='utf-8') as file:
            history = file.read()
            main = style + history + script
    else:
        with open("README.md", 'r', encoding='utf-8') as file:
            home = file.read()
            home =  home[home.find('## Usage'):]
            home = markdown.markdown(home, extensions=['fenced_code'])
            home = f'''
            <div class="box">
                {home}
            </div>
            '''
            main = style + home + script
    return main

if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    parser = argparse.ArgumentParser(description="Assistant parameters")
    parser.add_argument('--instance', type=str, help='Select model instance. Models available are: gpt, claude, llama and mistral')
    parser.add_argument('--prompt', type=str, help='Prompt text')
    args = parser.parse_args()

    if not any(vars(args).values()):
        main = build_main()
    else:
        if not args.instance:
            instance = choose_model("o3")
        else:
            instance = choose_model(args.instance)
        prompt = args.prompt
        chat_fetcher = ChatFetcher(instance)
        response = asyncio.run(chat_fetcher.fetch_response(prompt))

        current_time = datetime.now().strftime("%A, %B %d, %Y. %H:%M")
        body = f'''
        <div class="box">
            <p style="color: gray; font-size: small; display: flex; justify-content: space-between; width: 100%;">
                <span style="text-align: left;">{current_time}</span>
                <span style="text-align: right;">{instance}</span>
            </p>
            <br>
            <h1>{prompt[:prompt.find(" : ")]}</h1>
            <br>
            {response}
        </div>
        '''
        with open('history.html', 'a') as file:
            file.write(body)

        main = build_main()

    try:
        bus = dbus.SessionBus()
        runing_wv = bus.get_object(SERVICE, SERVICE_PATH)
        runing_wv.refresh_webview(main)
    except dbus.DBusException:
        wv = CreateWebView()
        service = refreshWebviewService(wv)
        wv.run(main)
