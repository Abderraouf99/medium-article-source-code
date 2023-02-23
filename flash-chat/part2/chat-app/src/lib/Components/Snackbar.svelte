<script lang="ts">
  import { InlineNotification } from "carbon-components-svelte";
  import type { SnackbarMessage } from "../models/snackbar-message";

  export let snackbarMessage: SnackbarMessage;
  $: {
    if (snackbarMessage.show) {
      setTimeout(() => {
        snackbarMessage.show = false;
      }, 3000);
    }
  }
</script>

{#if snackbarMessage.show}
  <div class="snackbar">
    <InlineNotification
      kind={snackbarMessage.kind}
      title={snackbarMessage.title}
      subtitle={snackbarMessage.message}
    />
  </div>
{/if}

<style>
  .snackbar {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
  }
</style>
