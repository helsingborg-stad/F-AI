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

  interface Document {
    id: string;
    name: string;
  }

  export let endpoint: string;
  export let documents: Document[];

  let selectedDocument: string;
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

      eventSource = new EventSource(`${endpoint}?question=${question}&document=${selectedDocument}`);
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

<Div class="flex gap-5 p-5 flex-col items-center justify-center h-full overflow-hidden grow">

  <!-- Document picker -->
  <select
    class="select select-bordered w-full max-w-xs"
    bind:value={selectedDocument}>
    <option disabled selected value="">Välj dokument</option>
    {#each documents as document (document.id)}
      <option value={document.id}>{document.name}</option>
    {/each}
  </select>

  <!-- Content -->
  <Div class="w-full grow flex flex-col gap-2 items-center justify-center overflow-hidden">

    <!-- Chat bubbles -->
    <div class="grow w-full max-w-prose">
      {#each messages as message (message.id)}
        <ChatBubble
          user={message.user}
          content={message.content}
          time={message.time}
          isSelf={message.isSelf}
        />
      {:else}
        <div class="flex flex-col items-center justify-center">
          <p>Här kan du ställa direkta frågor angående dokument du har laddat upp.</p>
          <p>Välj ett dokument för att börja.</p>
        </div>
      {/each}

      <span class="loading loading-spinner" class:opacity-0={!eventSource} />
    </div>

    <!-- Clear button -->
    {#if messages.length > 0}
      <Button
        onClick={() => messages = []}
        label="Rensa chat"
        state="secondary"
        disabled={!!eventSource} />
    {/if}
  </Div>

  <!-- Form controls -->
  <form class="w-full" on:submit|preventDefault={() => alert("bruh")}>
    <fieldset disabled={!selectedDocument}>
      <Div class="flex gap-2 w-full items-end">
        <textarea
          name="message"
          bind:value={currentMessageInput}
          class="textarea textarea-bordered grow"
        />
        <Button
          onClick={()=>createSSE(currentMessageInput)}
          label=""
          iconSrc="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXNlbmQiPjxwYXRoIGQ9Im0yMiAyLTcgMjAtNC05LTktNFoiLz48cGF0aCBkPSJNMjIgMiAxMSAxMyIvPjwvc3ZnPg=="
        />
      </Div>
    </fieldset>
  </form>
</Div>