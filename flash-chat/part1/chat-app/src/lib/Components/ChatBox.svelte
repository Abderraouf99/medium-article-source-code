<script>
  import {
    Tile,
    TextInput,
    Button,
    InlineNotification,
  } from "carbon-components-svelte";

  import Send from "carbon-icons-svelte/lib/Send.svelte";
  import { onDestroy, onMount } from "svelte";

  let messageText = "";
  let senderId = "";

  let messages = [];

  let socket;

  let snackBarMessage = "Connected";
  let snackBarStatus = "Success";
  let showSnackBar = false;

  onMount(() => {
    try {
      socket = new WebSocket("ws://localhost:8000/messaging");

      socket.onopen = (ws, event) => {
        console.log("connected");
        handleShowSnackBar("Connected", "Success");
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data["type"] == "connect") {
            senderId = data["id"];
          } else if (data["type"] == "disconnected") {
            handleShowSnackBar("Disconnected", `Client ` + data["id"]);
          } else {
            messages = [data, ...messages];
          }
        } catch (e) {
          console.log(event.data);
          console.error(e);
        }
      };

      socket.onerror = (event) => {
        console.log("Failed to connect to websocket");
      };

      socket.close = (event) => {
        handleShowSnackBar("Disconnected", "Client disconnected");
        console.log("Connection closed");
      };
    } catch (e) {
      console.log("Failed to connect to websocket");
    }
  });

  onDestroy(() => {
    try {
      socket.close();
    } catch (e) {
      console.log("Failed to close socket");
    }
  });

  function handleSendMessage() {
    if (messageText == "") return;
    socket.send(JSON.stringify({ text: messageText, senderId: senderId }));

    messageText = "";
  }

  function handleShowSnackBar(message, status) {
    showSnackBar = true;
    snackBarMessage = message;
    snackBarStatus = status;
    setTimeout(() => {
      showSnackBar = false;
    }, 3000);
  }
</script>

<Tile style="width: 500px; height: 700px">
  <p>ID: {senderId}</p>
  <div class="tile-header">
    <h2>Flash Chat</h2>
  </div>

  <div class="messages-history">
    {#if messages.length == 0}
      <p style="position: absolute; top: 50%; left: 50%; translate: -50%">
        There are no messages yet
      </p>
    {/if}
    {#each messages as message}
      {#if message.senderId == senderId}
        <div class=" message-tile align-right">
          <p>
            {message.text}
          </p>
        </div>
      {:else}
        <div class="message-tile align-left">
          <p>
            {message.text}
          </p>
        </div>
      {/if}
    {/each}
  </div>
  <div class="tile-actions">
    <TextInput
      labelText="Message"
      placeholder="Enter a message..."
      bind:value={messageText}
    />
    <Button type="submit" on:click={handleSendMessage} icon={Send}>Send</Button>
  </div>
</Tile>

{#if showSnackBar}
  <div class="snackbar">
    <InlineNotification
      kind="info"
      title={snackBarStatus}
      subtitle={snackBarMessage}
    />
  </div>
{/if}

<style>
  .tile-header {
    display: flex;
    padding: 10px 0px 10px 0px;
    justify-content: space-between;
  }
  .messages-history {
    position: relative;
    display: flex;
    flex-direction: column-reverse;
    padding: 10px 0px 10px 0px;
    min-height: 0;
    height: calc(0.7 * 700px);
    width: 100%;
    overflow-y: scroll;
    overflow-x: hidden;
  }
  .tile-actions {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin-top: 20px;
  }

  .message-tile {
    padding: 20px;
    max-width: 50%;
    margin: 10px 0px 10px 0px;
  }

  .align-right {
    position: relative;
    left: 100%;
    translate: -105%;
    background-color: #0f62fe;
    margin-right: 10px;
  }

  .align-left {
    background-color: #6f6f6f;
  }
  .snackbar {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
  }
</style>
