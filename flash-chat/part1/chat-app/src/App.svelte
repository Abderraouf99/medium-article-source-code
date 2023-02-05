<script lang="ts">
  import ChatBox from "./lib/Components/ChatBox.svelte";
  import "carbon-components-svelte/css/g100.css";
</script>

<main>
  <div class="centered-chat-box">
    <ChatBox />
  </div>
</main>

<style>
  .centered-chat-box {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
  }
</style>
