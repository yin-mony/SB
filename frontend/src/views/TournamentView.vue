<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <main class="max-w-7xl mx-auto px-6 py-20">
      <header class="mb-24 flex flex-col items-center">
        <h2 class="text-7xl humor-font font-black mb-8">
          辩论 <span class="bg-mint text-black px-6 border-4 border-black inline-block rotate-[-2deg]">副本指南</span>
        </h2>
        <p class="text-3xl font-black text-slate-700 italic">如何像职业杠精一样优雅地通关？</p>
      </header>

      <div class="space-y-16 relative">
        <div class="absolute left-1/2 top-0 bottom-0 w-4 bg-black hidden md:block rounded-full"></div>

        <div class="flex flex-col md:flex-row items-center gap-12 relative">
          <div class="md:w-1/2 flex justify-end">
            <div class="format-card bg-white p-10 rounded-[3rem] max-w-lg relative rotate-[-1deg]">
              <span class="step-number">01</span>
              <h3 class="text-4xl font-black mb-6 text-pink-500">第一关：华丽登场 (立论)</h3>
              <p class="text-xl font-bold leading-relaxed mb-6">
                这是你建立世界观的时刻。用三分钟时间告诉大家为什么你的观点是正确的，顺便展示一下你丰富的词汇量（即便有些是胡编乱造的）。
              </p>
              <div class="bg-black text-white p-4 rounded-2xl flex items-center gap-3">
                <Icon class="text-yellow-400" icon="mdi:sword" width="30"></Icon>
                <span class="font-black">技能建议：一本正经的胡说八道 (Lv. MAX)</span>
              </div>
            </div>
          </div>
          <div class="md:w-1/2">
            <Icon class="text-pink-500 text-9xl rotate-12 drop-shadow-[5px_5px_0px_black]" icon="mdi:flag-variant"></Icon>
          </div>
        </div>

        <div class="flex flex-col md:flex-row-reverse items-center gap-12 relative">
          <div class="md:w-1/2 flex justify-start">
            <div class="format-card bg-yellow-400 p-10 rounded-[3rem] max-w-lg relative rotate-[1deg]">
              <span class="step-number text-black opacity-10">02</span>
              <h3 class="text-4xl font-black mb-6 text-black">第二关：闪避与反击 (驳论)</h3>
              <p class="text-xl font-bold leading-relaxed mb-6">
                对手刚刚说完他的观点，现在轮到你把他的逻辑拆成零件，然后再组装成一架纸飞机扔回去。记住：先肯定对方，然后再说“但是”。
              </p>
              <div class="bg-white text-black border-4 border-black p-4 rounded-2xl flex items-center gap-3">
                <Icon class="text-blue-500" icon="mdi:shield-bug" width="30"></Icon>
                <span class="font-black">技能建议：这你也能信？ (防御技能)</span>
              </div>
            </div>
          </div>
          <div class="md:w-1/2 flex justify-end">
            <Icon class="text-yellow-500 text-9xl -rotate-12 drop-shadow-[5px_5px_0px_black]" icon="mdi:lightning-bolt"></Icon>
          </div>
        </div>

        <div class="flex flex-col md:flex-row items-center gap-12 relative">
          <div class="md:w-1/2 flex justify-end">
            <div class="format-card bg-blue-500 text-white p-10 rounded-[3rem] max-w-lg relative rotate-[-1deg]">
              <span class="step-number text-white opacity-20">03</span>
              <h3 class="text-4xl font-black mb-6 text-yellow-300">第三关：一锤定音 (结辩)</h3>
              <p class="text-xl font-bold leading-relaxed mb-6">
                最后的表演时间！把刚才所有的争论揉在一起，升华到宇宙的高度。无论刚才吵成什么样，现在你要表现得像个智者一样。
              </p>
              <div class="bg-pink-600 text-white p-4 rounded-2xl flex items-center gap-3 shadow-[4px_4px_0px_white]">
                <Icon class="text-yellow-400" icon="mdi:star-face" width="30"></Icon>
                <span class="font-black">技能建议：升华到星辰大海 (满分谢幕)</span>
              </div>
            </div>
          </div>
          <div class="md:w-1/2">
            <Icon class="text-blue-500 text-9xl rotate-12 drop-shadow-[5px_5px_0px_black]" icon="mdi:trophy-variant"></Icon>
          </div>
        </div>
      </div>

      <div class="mt-32 format-card bg-black text-white p-16 rounded-[4rem] text-center border-b-8 border-pink-500">
        <h3 class="text-5xl humor-font font-black mb-10">通关奖励是什么？</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div class="p-6 border-4 border-white/20 rounded-3xl hover:border-pink-500 transition-colors">
            <p class="text-6xl mb-4">👑</p>
            <p class="text-2xl font-black mb-2">杠精皇冠</p>
            <p class="text-slate-400 font-bold">可以让你的 ID 在评论区发光五分钟。</p>
          </div>
          <div class="p-6 border-4 border-white/20 rounded-3xl hover:border-yellow-400 transition-colors">
            <p class="text-6xl mb-4">🍕</p>
            <p class="text-2xl font-black mb-2">虚拟披萨</p>
            <p class="text-slate-400 font-bold">不能吃，但看着挺香的，有助于缓解辩论后的饥饿感。</p>
          </div>
          <div class="p-6 border-4 border-white/20 rounded-3xl hover:border-blue-400 transition-colors">
            <p class="text-6xl mb-4">💖</p>
            <p class="text-2xl font-black mb-2">对手的尊重</p>
            <p class="text-slate-400 font-bold">虽然他可能不承认，但你的胡说八道深深折服了他。</p>
          </div>
        </div>
      </div>
    </main>

    <footer class="bg-black py-10 text-white mt-20">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center space-x-2">
          <Icon class="text-pink-500" icon="mdi:emoticon-tongue-outline" width="30"></Icon>
          <span class="text-xl humor-font font-bold">思辩乐园 (2026)</span>
        </div>
        <p class="text-slate-400 font-bold">© 2026 既然你都看到这里了，不如去参加一场辩论吧？</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import FloatingNav from '../components/layout/FloatingNav.vue'
import MainNav from '../components/layout/MainNav.vue'
</script>

<style>
.format-card {
  border: 4px solid black;
  box-shadow: 10px 10px 0px black;
  transition: all 0.3s;
}

.format-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 14px 14px 0px black;
}
</style>
