from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import StreamingResponse, Response
import faiss
import threading
import queue
import pickle
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQAWithSourcesChain

note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)


def llm_thread(g, prompt):
    try:
        llm = ChatOpenAI(
            openai_api_key='YOUR_KEY',
            model_name='gpt-3.5-turbo-0301',
            verbose=True,
            streaming=True,
            callback_manager=AsyncCallbackManager([ChainStreamHandler(g)]),
            temperature=0,
        )
        
        # Load the LangChain.
        index = faiss.read_index("/home/talha/Documents/FastAPI tutorial/chatmodel/docs.index")
        with open("/home/talha/Documents/FastAPI tutorial/chatmodel/faiss_store.pkl", "rb") as f:
            store = pickle.load(f)
        store.index = index

        chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, retriever=store.as_retriever())
        chain({'question': prompt})

    finally:
        g.close()


def chat(prompt):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, prompt)).start()
    return g


@note.post("/query")
async def stream(request: Request):
    form = await request.form()
    question = form.get('question')
    return StreamingResponse(chat(question), media_type='text/event-stream')
