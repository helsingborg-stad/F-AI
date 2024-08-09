# LLM Worker

This is a python application that runs LLM jobs (remote and local supported)
using assistant templates and communicates via websockets.

## Start

1. Setup dependencies with [poetry](https://python-poetry.org/)
2. run `run.sh`

## Example

Using [websocat](https://github.com/vi/websocat), connect to the endpoint (with
the address/port from `.env` file):

```bash
websocat ws://LISTEN_ADDRESS:LISTEN_PORT/ws/
```

Send one of the following string payloads:

### "add" request

Queues an LLM job to be done as soon as the worker is available.

```json
{
  "type": "add",
  "id": "my-custom-id",
  "query": "How tall is it?",
  "assistant": {
    "streams": [
      {
        "provider": "openai",
        "settings": {
          "model": "gpt-3.5-turbo"
        },
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful assistant."
          },
          {
            "insert": "history"
          },
          {
            "role": "user",
            "content": "{query}"
          }
        ]
      }
    ]
  },
  "history": [
    {
      "role": "user",
      "content": "Where is the eiffel tower?"
    },
    {
      "role": "system",
      "content": "The Eiffel Tower is located in Paris, France."
    }
  ]
}
```

If accepted, the server will respond with a mapping of your provided job id
to an opaque id that will be used in subsequent messages to refer to your job:

<!-- @formatter:off -->
```json
{"type": "resp_add","id": "my-custom-id","job_id": "94bdccf2-238f-4c90-9858-b506f9f3397d"}
```
<!-- @formatter:on -->

The server will automatically register the client for callbacks to that job id,
same as if the client sent a "listen" request (see below).

### "listen" request

Listen for updates regarding a specific job.

<!-- @formatter:off -->
```json
{"type": "listen","job_id": "94bdccf2-238f-4c90-9858-b506f9f3397d"}
```
<!-- @formatter:on -->

The server will then send back updates of the job as they occur:

<!-- @formatter:off -->
```json lines
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":""}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":""}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":"The"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" E"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":"iff"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":"el"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" Tower"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" is"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" approximately"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" "}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":"1"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":","}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":"063"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" feet"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" ("}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":"324"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" meters"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":")"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" tall"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":","}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" including"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" antennas"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" at"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" the"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":" top"}
{"type":"running","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":"."}
{"type":"done","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d"}
```
<!-- @formatter:on -->

In case a handled error occurs an error message will be sent:

<!-- @formatter:off -->
```json
{"type":"failed","job_id":"94bdccf2-238f-4c90-9858-b506f9f3397d","message":"test error"}
```
<!-- @formatter:on -->

In case of other (unhandled) errors the connection will probably just forcefully
close.