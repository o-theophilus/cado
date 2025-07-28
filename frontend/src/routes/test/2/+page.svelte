<script>
  let isDrawn = false;
  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  
  function startAnimation() {
    isDrawn = true;
  }
</script>

<svg width="40" height="40" viewBox="0 0 120 120">
  <circle
    cx="60"
    cy="60"
    r={radius}
    fill="none"
    stroke="#3b82f6"
    stroke-width="8"
    stroke-dasharray={circumference}
    stroke-dashoffset={isDrawn ? 0 : circumference}
    style="transform: rotate(-90deg);
           transform-origin: 60px 60px;
           transition: stroke-dashoffset 2s ease-in-out;"
  />
</svg>

<button on:click={startAnimation}>Draw Circle</button>