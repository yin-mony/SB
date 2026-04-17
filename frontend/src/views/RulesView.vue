<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <main class="max-w-6xl mx-auto px-6 py-20">
      <div
        class="flex flex-col md:flex-row items-center gap-10 mb-20 bg-pink-500 text-white p-12 rounded-[4rem] border-8 border-black shadow-[20px_20px_0px_black] rotate-[-1deg]"
      >
        <div class="flex-1">
          <h2 class="text-6xl md:text-8xl humor-font font-black mb-6">思辩生存 <span class="text-yellow-400">圣经</span></h2>
          <p class="text-2xl font-black">别把这些当成真正的规则，它们更像是某种来自神秘力量的温馨提示（警告）。</p>
        </div>
        <div class="w-64 h-64 bg-white rounded-full flex items-center justify-center p-4 border-4 border-black animate-spin" style="animation-duration: 10s">
          <Icon class="text-pink-500" icon="mdi:alert-octagon" width="180"></Icon>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
        <div class="neo-brutalism-card bg-white p-10 rounded-[2rem] transform hover:scale-105 transition-transform">
          <span class="rule-badge">法则 01</span>
          <h3 class="text-3xl font-black mb-6 flex items-center gap-3">
            禁止降智打击 <Icon class="text-blue-500" icon="mdi:head-snowflake-outline"></Icon>
          </h3>
          <p class="text-xl font-bold text-slate-600 leading-relaxed">
            你可以试图说服对方，甚至可以试图绕晕对方，但绝对不能使用“你是不是傻”这种低级招数。高级的降智打击是通过引用不存在的量子物理学概念让对方怀疑人生。
          </p>
        </div>

        <div class="neo-brutalism-card bg-yellow-300 p-10 rounded-[2rem] transform rotate-[1deg] hover:rotate-0 transition-all">
          <span class="rule-badge">法则 02</span>
          <h3 class="text-3xl font-black mb-6 flex items-center gap-3">
            错字也是战术 <Icon class="text-black" icon="mdi:format-text-variant"></Icon>
          </h3>
          <p class="text-xl font-bold text-slate-800 leading-relaxed">
            如果在辩论中出现错别字，你可以解释为“这是密码学防御”。如果你对手指出你的错字，你可以反驳他：“你的格局太小了，只看得到文字，看不到星辰大海”。
          </p>
        </div>

        <div class="neo-brutalism-card bg-mint p-10 rounded-[2rem] transform rotate-[-1deg] hover:rotate-0 transition-all">
          <span class="rule-badge">法则 03</span>
          <h3 class="text-3xl font-black mb-6 flex items-center gap-3">
            保护你的猫狗 <Icon class="text-pink-600" icon="mdi:cat"></Icon>
          </h3>
          <p class="text-xl font-bold text-slate-800 leading-relaxed">
            正如我们的价值观所言，辩论到高潮处不准摔键盘，不准掀桌子，更不准吓坏身边的猫。任何导致宠物受惊的辩论行为都将被判定为“违规操作”。
          </p>
        </div>

        <div class="neo-brutalism-card bg-purple-500 text-white p-10 rounded-[2rem] transform hover:scale-105 transition-transform">
          <span class="rule-badge bg-white text-black">法则 04</span>
          <h3 class="text-3xl font-black mb-6 flex items-center gap-3 text-yellow-300">
            承认失败不可耻 <Icon class="text-white" icon="mdi:flag-checkered"></Icon>
          </h3>
          <p class="text-xl font-bold leading-relaxed">
            如果你被对方说服了，请体面地发一张“大佬牛逼”的表情包。承认对方有趣，是最高级的辩论礼仪。当然，你也可以在心里默默地想“他只是今天运气好”。
          </p>
        </div>
      </div>

      <div class="mt-20 neo-brutalism-card bg-black p-12 rounded-[3rem] text-center text-white relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-full pointer-events-none">
          <div class="bg-pink-500 w-20 h-20 absolute top-5 right-10 rounded-full mix-blend-screen opacity-50 blur-xl"></div>
          <div class="bg-blue-500 w-32 h-32 absolute bottom-5 left-10 rounded-full mix-blend-screen opacity-50 blur-xl"></div>
        </div>
        <h3 class="text-4xl humor-font font-black mb-6 text-mint">终极禁忌</h3>
        <p class="text-2xl font-bold max-w-2xl mx-auto leading-loose">
          绝对、绝对、绝对禁止在“思辩乐园”里讨论“明天吃什么”。<br />
          因为这个问题没有终点，会耗尽宇宙的所有能量。
        </p>
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
.neo-brutalism-card {
  border: 4px solid black;
  box-shadow: 12px 12px 0px black;
}

.rule-badge {
  display: inline-block;
  padding: 4px 12px;
  background: black;
  color: white;
  font-weight: 900;
  border-radius: 99px;
  margin-bottom: 12px;
}
</style>
