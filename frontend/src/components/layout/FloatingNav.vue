<template>
  <div class="floating-nav">
    <RouterLink class="floating-nav-item bg-pink-400" to="/rules">
      <Icon icon="mdi:gavel" width="32" />
      <span class="tooltip">游玩规则</span>
    </RouterLink>
    <RouterLink class="floating-nav-item bg-yellow-400" to="/tournament">
      <Icon icon="mdi:trophy-variant" width="32" />
      <span class="tooltip">巅峰赛制</span>
    </RouterLink>
    <RouterLink class="floating-nav-item bg-blue-400" to="/resources">
      <Icon icon="mdi:tools" width="32" />
      <span class="tooltip">秘密武器</span>
    </RouterLink>
    <RouterLink class="floating-nav-item bg-green-400" to="/about">
      <Icon icon="mdi:information-variant" width="32" />
      <span class="tooltip">关于我们</span>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style>
.floating-nav {
  position: fixed;
  right: 2rem;
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.floating-nav-item {
  width: 64px;
  height: 64px;
  background: white;
  border: 3px solid black;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 4px 4px 0px black;
  position: relative;
}

.floating-nav-item:hover {
  transform: scale(1.2) rotate(5deg);
  background: var(--secondary);
  box-shadow: 6px 6px 0px black;
}

.floating-nav-item .tooltip {
  position: absolute;
  right: 80px;
  background: black;
  color: white;
  padding: 4px 12px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 14px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
}

.floating-nav-item:hover .tooltip {
  opacity: 1;
}

@media (max-width: 768px) {
  .floating-nav {
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
    transform: none;
    flex-direction: row;
    justify-content: space-around;
    background: white;
    padding: 10px;
    border-top: 4px solid black;
    width: 100%;
  }

  .floating-nav-item {
    width: 50px;
    height: 50px;
    box-shadow: 2px 2px 0px black;
  }

  .floating-nav-item .tooltip {
    display: none;
  }
}
</style>
