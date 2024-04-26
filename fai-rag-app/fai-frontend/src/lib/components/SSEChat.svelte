<script lang="ts">
  import Div from "./Div.svelte";
  import Button from "./Button.svelte";
  import ChatBubble from "./ChatBubble.svelte";

  interface SSEMessage {
    type: string;
    date: string;
    source: string | null;
    content: string | null;
  }

  interface ChatMessage {
    id: string;
    user: string;
    content: string;
    time: string;
    isSelf: boolean;
  }

  export let endpoint: string;
  let messages: ChatMessage[] = [];
  let currentMessageInput: string = "";
  let eventSource: EventSource | null = null;

  function addErrorMessage(message: string) {
    messages = [...messages, {
      id: `error${messages.length}`,
      user: "Error",
      content: message,
      time: new Date().toTimeString().split(" ")[0],
      isSelf: false
    }];
  }


  function toChatMessage(sse: SSEMessage): ChatMessage {
    return {
      id: sse.date,
      user: sse.source ?? "",
      content: sse.content ?? "",
      time: sse.date,
      isSelf: false
    };
  }


  function processRawSSEEvent(rawData: string) {
    try {
      const rEvent = /event: (.*)\n/;
      const rData = /data: (.*)\n\n/;

      const eventMatch = rEvent.exec(rawData);
      if (!eventMatch) {
        return;
      }

      const event = eventMatch[1];

      if (event == "message_end") {
        console.log("got end of message");
        eventSource?.close();
        eventSource = null;
        return;
      }

      if (event == "message") {
        const dataMatch = rData.exec(rawData);
        const b64string = dataMatch![1];
        const bytes = Uint8Array.from(atob(b64string), (m) => m.codePointAt(0)!);
        const jsonString = new TextDecoder().decode(bytes);
        const messagePayload = JSON.parse(jsonString) as SSEMessage;
        const chatMessage = toChatMessage(messagePayload);

        messages = [...messages.slice(0, -1), {
          ...messages.at(-1),
          ...chatMessage,
          content: messages.at(-1)!.content + chatMessage.content
        }];
      }
    } catch (e) {
      console.error("Failed to parse raw message", e);
      eventSource?.close();
    }
  }


  function createSSE(question: string) {
    try {
      if (question.length == 0) return;
      currentMessageInput = "";

      messages = [...messages, {
        id: `self${messages.length}`,
        isSelf: true,
        user: "Me",
        content: question,
        time: new Date().toTimeString().split(" ")[0]
      }, {
        id: `placeholder${messages.length}`,
        isSelf: false,
        user: "",
        content: "",
        time: ""
      }];

      eventSource?.close();
      eventSource = null;

      eventSource = new EventSource(`${endpoint}?question=${question}`);
      eventSource.onmessage = (e) => processRawSSEEvent(e.data);
      eventSource.onerror = (e) => {
        addErrorMessage(`unknown error / ${e}`);
        eventSource?.close();
        eventSource = null;
      };
      console.log("sse up");
    } catch (e) {
      eventSource?.close();
      eventSource = null;
      addErrorMessage(e?.toString() ?? "unknown");
    }
  }
</script>

<Div class="flex flex-col items-center justify-center">
  <Div class="w-full flex flex-col items-center justify-center my-5">
    {#each messages as message (message.id)}
      <ChatBubble
        user={message.user}
        content={message.content}
        time={message.time}
        isSelf={message.isSelf}
      />
    {:else}
      <p class="py-20">Inga meddelanden kompis. Fråga mig nåt!</p>
    {/each}
  </Div>
  <Div class="flex gap-2 w-full">
    <span class="loading loading-spinner" class:opacity-0={!eventSource} />
    <input
      class="input input-bordered grow"
      bind:value={currentMessageInput}
      type="text"
      name="message"
      placeholder="Meddelande"
      data-1p-ignore
    />
    <Button
      onClick={()=>createSSE(currentMessageInput)}
      label=""
      iconSrc="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXNlbmQiPjxwYXRoIGQ9Im0yMiAyLTcgMjAtNC05LTktNFoiLz48cGF0aCBkPSJNMjIgMiAxMSAxMyIvPjwvc3ZnPg=="
    />
  </Div>
</Div>