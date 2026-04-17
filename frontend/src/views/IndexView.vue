<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />

    <div class="abstract-shape bg-pink-400 w-96 h-96 top-[-10%] left-[-10%] rounded-full"></div>
    <div
      class="abstract-shape bg-yellow-300 w-80 h-80 bottom-[-5%] right-[-5%] rounded-full"
      style="animation-delay: -2s"
    ></div>
    <div class="abstract-shape bg-blue-400 w-64 h-64 top-[40%] right-[10%] rounded-full" style="animation-delay: -5s"></div>

    <MainNav />

    <main class="relative z-10 min-h-[calc(100vh-6rem)] flex flex-col items-center justify-center text-center px-6">
      <div class="max-w-4xl space-y-10">
        <div class="inline-block px-6 py-2 bg-black text-yellow-400 rounded-full text-lg font-black rotate-[-2deg] mb-4">
          🚀 {{ homeDateLine }} · 今天宜：抬杠
        </div>
        <h2 class="text-7xl md:text-8xl humor-font font-black leading-none tracking-tight">
          欢迎来到 <span class="text-pink-500 underline decoration-black decoration-8">思辩乐园</span>！<br />
          <span class="text-blue-600">这里没有严肃，</span><br />
          <span class="text-green-500">只有有趣的碰撞~</span>
        </h2>
        <p class="text-2xl md:text-3xl font-bold text-slate-700 max-w-2xl mx-auto leading-relaxed">
          别再像在课堂上那样皱眉头啦！来这里，把逻辑当成飞镖，把证据当成爆米花，让我们在知识的海洋里打个漂亮的“水漂”！
        </p>
        <div class="pt-8 flex flex-col items-center gap-6">
          <RouterLink
            class="bg-purple-600 text-white text-3xl font-black px-12 py-8 rounded-3xl bouncy-btn border-4 border-black shadow-[12px_12px_0px_black] wiggle"
            to="/debate-list"
          >
            🏊‍♂️ 跳进话题池！
          </RouterLink>
          <p class="text-slate-400 font-bold italic animate-bounce">别害羞，底下水温刚刚好 (指正反方吵得很凶) 👇</p>
        </div>
      </div>

      <Icon
        class="absolute top-[20%] left-[10%] text-yellow-500 opacity-30 animate-pulse"
        icon="mdi:duck"
        width="100"
      />
      <Icon
        class="absolute bottom-[20%] right-[15%] text-pink-500 opacity-30 animate-bounce"
        icon="mdi:balloon"
        width="80"
      />
      <Icon class="absolute top-[60%] left-[20%] text-purple-500 opacity-20" icon="mdi:brain" width="120" />
    </main>

    <footer class="bg-black py-10 text-white mt-20">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center space-x-2">
          <Icon class="text-pink-500" icon="mdi:emoticon-tongue-outline" width="30"></Icon>
          <span class="text-xl humor-font font-bold">思辩乐园 ({{ currentYear }})</span>
        </div>
        <p class="text-slate-400 font-bold">© {{ currentYear }} 这里的所有观点都是为了好玩。如有雷同，纯属巧合。</p>
        <div class="flex gap-8 text-2xl">
          <RouterLink class="hover:text-pink-500 transition-colors" to="/debate-list" title="辩论广场">
            <Icon icon="mdi:ghost"></Icon>
          </RouterLink>
          <RouterLink class="hover:text-yellow-400 transition-colors" to="/blog" title="胡说博客">
            <Icon icon="mdi:ufo-outline"></Icon>
          </RouterLink>
          <RouterLink class="hover:text-blue-400 transition-colors" to="/rules" title="游玩守则">
            <Icon icon="mdi:robot-mop-outline"></Icon>
          </RouterLink>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import FloatingNav from '../components/layout/FloatingNav.vue'
import MainNav from '../components/layout/MainNav.vue'

const pad2 = (n) => String(n).padStart(2, '0')

const homeDateLine = ref('')
const currentYear = ref(new Date().getFullYear())

const syncHomeClock = () => {
  const d = new Date()
  homeDateLine.value = `${d.getFullYear()}.${pad2(d.getMonth() + 1)}.${pad2(d.getDate())}`
  currentYear.value = d.getFullYear()
}

let homeClockTimer = null

onMounted(() => {
  syncHomeClock()
  homeClockTimer = window.setInterval(syncHomeClock, 60_000)
})

onUnmounted(() => {
  if (homeClockTimer != null) window.clearInterval(homeClockTimer)
})
</script>

<style>
body {
  overflow-x: hidden;
}

.abstract-shape {
  position: absolute;
  z-index: 0;
  filter: blur(40px);
  opacity: 0.6;
  animation: float 10s infinite alternate;
}

@keyframes float {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
  }
  100% {
    transform: translate(50px, 30px) rotate(15deg) scale(1.1);
  }
}

.bouncy-btn {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.1) rotate(-3deg);
  box-shadow: 10px 10px 0px rgba(0, 0, 0, 0.1);
}

.wiggle:hover {
  animation: wiggle 0.5s ease-in-out infinite;
}

@keyframes wiggle {
  0%,
  100% {
    transform: rotate(-2deg);
  }
  50% {
    transform: rotate(2deg);
  }
}
</style>
