# PyFrameX 🚀

PyFrameX is a **minimal educational Python framework** built to understand
how real-world frameworks like FastAPI and Django work internally.

## Features
- Dependency Injection
- Routing with decorators
- Middleware (sync + async)
- Context system
- Plugin architecture
- ASGI HTTP binding
- Async support

## Installation
```bash
pip install -e .

## basic app


📌 Keep it **honest and educational**.

---

## 🧱 STEP 6 — Add an Example App

### `examples/basic_app.py`

```python
from pyframex.container import Container
from pyframex.router import Router
from pyframex.app import App
from pyframex.config import Config
from pyframex.response import Response
from pyframex.asgi import ASGIAdapter

container = Container()
container.register("router", Router, singleton=True)

router = container.resolve("router")

@router.route("/")
async def home(ctx):
    return Response.text("Hello from PyFrameX")

app = App(container, Config(debug=True))
app.load_plugins()

asgi_app = ASGIAdapter(router)

uvicorn examples.basic_app:asgi_app
