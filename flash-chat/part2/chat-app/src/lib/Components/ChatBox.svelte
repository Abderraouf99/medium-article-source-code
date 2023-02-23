<script lang="ts">
  import { Tile, TextInput, Button } from "carbon-components-svelte";

  import Send from "carbon-icons-svelte/lib/Send.svelte";
  import { onDestroy, onMount } from "svelte";

  let messageText: string = "";
  let senderId: string = "";

  let messages = [];

  let socket;

  onMount(() => {
    // try {
    //   socket = new WebSocket("ws://localhost:8000/messaging");
    //   socket.onopen = (ws, event) => {
    //     console.log("connected");
    //     handleShowSnackBar("Connected", "Success");
    //   };
    //   socket.onmessage = (event) => {
    //     try {
    //       const data = JSON.parse(event.data);
    //       if (data["type"] == "connect") {
    //         senderId = data["id"];
    //       } else if (data["type"] == "disconnected") {
    //         handleShowSnackBar("Disconnected", `Client ` + data["id"]);
    //       } else {
    //         messages = [data, ...messages];
    //       }
    //     } catch (e) {
    //       console.log(event.data);
    //       console.error(e);
    //     }
    //   };
    //   socket.onerror = (event) => {
    //     console.log("Failed to connect to websocket");
    //   };
    //   socket.close = (event) => {
    //     handleShowSnackBar("Disconnected", "Client disconnected");
    //     console.log("Connection closed");
    //   };
    // } catch (e) {
    //   console.log("Failed to connect to websocket");
    // }
  });

  onDestroy(() => {
    // try {
    //   socket.close();
    // } catch (e) {
    //   console.log("Failed to close socket");
    // }
  });

  function handleSendMessage() {
    if (messageText == "") return;
    socket.send(JSON.stringify({ text: messageText, senderId: senderId }));

    messageText = "";
  }
</script>

<div class="message-list">
  {#if messages.length > 0}
    {#each messages as message}
      <div class="message">
        <div class="message-sender">{message.senderId}</div>
        <div class="message-text">{message.text}</div>
      </div>
    {/each}
  {:else}
    <div class="no-messages">No messages</div>
  {/if}
</div>
<div class="tile-actions">
  <TextInput labelText="Message" placeholder="Enter a message..." />
  <Button type="submit" icon={Send}>Send</Button>
</div>

<style>
  .message-list {
    height: 500px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow-y: scroll;
    overflow-x: hidden;
  }
  .tile-actions {
    display: flex;
    align-items: flex-end;
    padding: 10px;
  }
  .no-messages {
    text-align: center;
    padding: 10px;
  }
</style>
