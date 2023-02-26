<script lang="ts">
  import ChatBox from "./lib/Components/ChatBox.svelte";
  import "carbon-components-svelte/css/g100.css";
  import UserName from "./lib/Components/UserName.svelte";
  import ChatView from "./lib/Components/ChatView.svelte";

  let userName: string = "";
  function handleUsernameEvent(event: CustomEvent<string>) {
    console.log("username submitted");
    userName = event.detail["userName"];
    console.log(userName);
  }
</script>

<main>
  {#if !userName}
    <div class="centered-chat-box">
      <UserName on:username={handleUsernameEvent} />
    </div>
  {:else}
    <div class="centered-chat-box">
      <ChatView {userName} />
    </div>
  {/if}>
</main>

<style>
  .centered-chat-box {
    display: flex;
    height: 100vh;
    justify-content: center;
    align-items: center;
  }
</style>
