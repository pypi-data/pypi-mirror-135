# EZTea Web Framework

```
pip install eztea
```

## Usage

```python
from validr import T

from eztea.web import Application, ResponderContext, Router

router = Router()


@router.get("/")
def hello(
    ctx: ResponderContext,
    name: str = T.str.default("world"),
) -> T.dict(hello=T.str):
    return {"hello": name}


app = Application()
app.include_router(router)
```
