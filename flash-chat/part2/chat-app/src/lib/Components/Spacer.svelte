<script lang="ts">
  export let space: number = 0;
  export let orientation: "vertical" | "horizontal" = "vertical";

  function getStyle(): string {
    if (orientation == "vertical") {
      return `height: ${space}px;`;
    } else {
      return `width: ${space}px;`;
    }
  }
</script>

<div style={getStyle()} />
