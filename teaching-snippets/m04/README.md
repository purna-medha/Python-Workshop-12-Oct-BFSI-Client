# M04 — Connect independently running programs

Encode → publish → translate requests → call and interpret.

Read the numbered snippets in order. Every snippet is at most 40 physical lines.

| Snippet | Principle | How to use |
|---|---|---|
| [s01_json.py](s01_json.py) | Encode information for exchange | `uv run --extra dev python -m m04.s01_json` |
| [s02_catalog_api.py](s02_catalog_api.py) | Publish an interface | `uv run uvicorn m04.s02_catalog_api:app --port 8000` |
| [s03_order_api.py](s03_order_api.py) | Translate requests into application operations | `uv run uvicorn m04.s03_order_api:app --port 8000` |
| [s04_http_client.py](s04_http_client.py) | Call an interface and interpret its outcome | `uv run --extra dev python -m m04.s04_http_client` |

Run commands from the `current-course/teaching-snippets` folder. See the [course index](../README.md) for setup and API prerequisites.

## Prediction and demonstration

**Before revealing the result:** An unknown product and a stopped server both prevent checkout. Will they produce the same kind of failure?

**Teaching move:** Use an unknown ID, then stop the server. Trace where the caller distinguishes the outcomes. Use [s04_http_client.py](s04_http_client.py) as the worked example.

<details>
<summary>Reasoned answer</summary>

No. An unknown product produces an HTTP rejection; a stopped server produces a communication failure. Status checking happens before interpreting success data.

</details>

Finish by asking which part of the mechanism would stay useful in another application. The [Nano-Zon lab](../../projects/nano-zon/labs/m04/README.md) includes a small extension with no supplied answer.
