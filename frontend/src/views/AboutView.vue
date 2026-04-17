<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <main class="relative z-10 max-w-6xl mx-auto px-6 py-20">
      <div class="text-center mb-20">
        <h2 class="text-6xl md:text-8xl humor-font font-black mb-6 rotate-[-1deg]">
          谁在背后 <span class="bg-yellow-400 px-4 border-4 border-black inline-block rotate-[2deg]">搞事情？</span>
        </h2>
        <p class="text-2xl font-bold text-slate-700 max-w-3xl mx-auto">
          我们不是一家公司，也不是一个社团，我们是一群在凌晨两点因为纠结“番茄炒蛋到底是咸的还是甜的”而吵到失眠的无聊星人。
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-12 mb-24">
        <div class="neo-brutalism-card bg-white p-8 rounded-3xl text-center">
          <div class="w-32 h-32 bg-blue-400 border-4 border-black rounded-full mx-auto mb-6 flex items-center justify-center overflow-hidden">
            <Icon class="text-black" icon="mdi:robot-happy" width="80"></Icon>
          </div>
          <h3 class="text-3xl font-black mb-2">杠精之王·阿强</h3>
          <p class="text-pink-600 font-black mb-4 uppercase">Chief Arguing Officer</p>
          <p class="font-bold text-slate-600">曾连续48小时在网络上论证“键盘上的每一个键位都有其灵魂”，最终因为键盘漏电而停止。</p>
        </div>

        <div class="neo-brutalism-card bg-mint p-8 rounded-3xl text-center rotate-[1deg]">
          <div class="w-32 h-32 bg-yellow-400 border-4 border-black rounded-full mx-auto mb-6 flex items-center justify-center overflow-hidden">
            <Icon class="text-black" icon="mdi:cat" width="80"></Icon>
          </div>
          <h3 class="text-3xl font-black mb-2">逻辑黑洞·小美</h3>
          <p class="text-blue-700 font-black mb-4 uppercase">Head of Nonsense</p>
          <p class="font-bold text-slate-600">她的逻辑就像莫比乌斯环，你以为你赢了，其实你只是进入了她的下一个死循环。</p>
        </div>

        <div class="neo-brutalism-card bg-purple-400 p-8 rounded-3xl text-center rotate-[-1deg]">
          <div class="w-32 h-32 bg-pink-500 border-4 border-black rounded-full mx-auto mb-6 flex items-center justify-center overflow-hidden">
            <Icon class="text-white" icon="mdi:alien-outline" width="80"></Icon>
          </div>
          <h3 class="text-3xl font-black mb-2">熬夜冠军·大壮</h3>
          <p class="text-yellow-300 font-black mb-4 uppercase">Sleep Deprivation Specialist</p>
          <p class="font-bold text-white">负责维护服务器，或者说，负责在服务器崩溃时对着屏幕大喊“为什么不工作了！”</p>
        </div>
      </div>

      <div class="neo-brutalism-card bg-black text-white p-12 rounded-[3rem] mb-20 relative overflow-hidden">
        <div class="absolute top-[-20%] right-[-10%] opacity-20 rotate-12">
          <Icon icon="mdi:bullseye-arrow" width="300"></Icon>
        </div>
        <h3 class="text-5xl humor-font font-black mb-10 text-yellow-400">我们的核心价值观</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-10">
          <div class="space-y-4">
            <h4 class="text-3xl font-black flex items-center gap-3">
              <span class="bg-pink-500 w-10 h-10 rounded-lg flex items-center justify-center text-black">1</span>
              快乐第一，逻辑第二
            </h4>
            <p class="text-slate-400 text-lg">如果一段完美的论证让你不开心，那这段论证就是垃圾。我们支持所有能让人笑出来的诡辩。</p>
          </div>
          <div class="space-y-4">
            <h4 class="text-3xl font-black flex items-center gap-3">
              <span class="bg-blue-500 w-10 h-10 rounded-lg flex items-center justify-center text-black">2</span>
              万物皆可辩
            </h4>
            <p class="text-slate-400 text-lg">从宇宙大爆炸到昨天中午的盒饭，只要你敢提，我们就敢辩。甚至可以辩论“辩论本身是否有意义”。</p>
          </div>
        </div>
      </div>

      <div class="text-center">
        <p class="text-3xl font-black mb-8">想加入这个疯狂的实验室？</p>
        <button class="bg-mint border-4 border-black px-10 py-5 rounded-2xl text-2xl font-black bouncy-btn shadow-[8px_8px_0px_black]">📧 给我们发求救信号 (邮件)</button>
      </div>
    </main>

    <footer class="bg-black py-10 text-white mt-20">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center space-x-2">
          <Icon class="text-pink-500" icon="mdi:emoticon-tongue-outline" width="30"></Icon>
          <span class="text-xl humor-font font-bold">思辩乐园 (2026)</span>
        </div>
        <p class="text-slate-400 font-bold">© 2026 既然你都看到这里了，不如去参加一场辩论吧？</p>
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
import { RouterLink } from 'vue-router'
import FloatingNav from '../components/layout/FloatingNav.vue'
import MainNav from '../components/layout/MainNav.vue'
</script>

<style>
.neo-brutalism-card {
  background: white;
  border: 4px solid black;
  box-shadow: 12px 12px 0px black;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(-1deg);
}
</style>
