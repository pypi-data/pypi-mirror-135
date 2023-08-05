from aiohttp import ClientSession
from asyncio import get_event_loop, sleep
from .gateway import DiscordGateway
from .errors import ApiError
import asyncio

class Client:
    def __init__(self, loop:asyncio.AbstractEventLoop = None, intents:int = 513, log:bool = True):
        self.log = log
        self.intents = intents
        self.baseurl = "https://discord.com/api/v9"
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.ws = None
        self.session = ClientSession(loop = self.loop)
        
    def run(self, *args, **kwargs):
        """
        If you don't want use gateway.
        Please do like this. 
        `client.run("token", gateway = False)`
        """
        self.loop.run_until_complete(self.start(*args, **kwargs))
        
    def print(self, name, content):
        if self.log is True:
            print(f"[{name}]:{content}")
        
    async def start(self, token, gateway:bool = True):
        self.token = token
        await self.login()
        if gateway:
            await self.connect()
        
    def dispatch(self, name, *args, **kwargs):
        """Run a Specific function.
        
        Examples
        --------
        ```python
        client.dispatch("on_ready")
        
        @client.event
        async def on_ready():
          print("ready")
        ```
        """
        eventname = "on_" + name
        if hasattr(self, eventname):
            coro = getattr(self, eventname)
            self.loop.create_task(coro(*args, **kwargs))
            
    def event(self, coro):
        """
        This is send gateway event.
        Examples:
            client = Client()
        
            @client.event
            async def on_ready():
                print("ready")
            client.run("ToKeN")
        """
        setattr(self, coro.__name__, coro)
        return coro
        
    async def json_or_text(self, r):
        if r.headers["Content-Type"] == "application/json":
            return await r.json()
        
    async def ws_connect(self, url):
        return await self.session.ws_connect(url)
    
    async def login(self):
        self.user = await self.request("GET", "/users/@me")
    
    async def request(self, method:str, path:str, *args, **kwargs):
        headers = {
            "Authorization": f"Bot {self.token}"
        }
        if kwargs.get("json"):
            headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        for t in range(5):
            async with self.session.request(method, self.baseurl + path, *args, **kwargs) as r:
                if r.status == 429:
                    data = await r.json()
                    if data["global"] is True:
                        raise ApiError("Now api is limit. Wait a minute please.")
                    else:
                        await sleep(data["retry_after"])
                elif r.status == 404:
                    raise ApiError("Not Found Error")
                elif 300 > r.status >= 200:
                    return await self.json_or_text(r)
        
    async def connect(self):
        if self.ws is None:
            self.ws = await DiscordGateway.start_gateway(self)
            await self.ws.catch_message()
            while not self.ws.closed:
                await self.ws.catch_message()
