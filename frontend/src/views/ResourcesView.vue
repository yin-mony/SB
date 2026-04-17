<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <main class="max-w-7xl mx-auto px-6 py-20">
      <div class="mb-20 text-center relative">
        <div class="inline-block bg-yellow-400 border-4 border-black p-4 rotate-[-2deg] mb-8">
          <h2 class="text-6xl humor-font font-black">神兵利器仓库</h2>
        </div>
        <p class="text-2xl font-bold text-slate-600 max-w-2xl mx-auto">
          工欲善其事，必先找借口。这里有所有能让你在辩论场上瞬间逼格提升 1000% 的工具。
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div class="neo-card bg-white p-8 rounded-[2rem] flex flex-col group">
          <div class="h-48 bg-pink-100 rounded-2xl mb-6 flex items-center justify-center border-2 border-black group-hover:bg-pink-200 transition-colors">
            <Icon class="text-pink-500 text-8xl" icon="mdi:book-open-page-variant"></Icon>
          </div>
          <h3 class="text-3xl font-black mb-4">《诡辩词典》</h3>
          <p class="text-lg font-bold text-slate-500 mb-6 flex-grow">教你如何把“我不确定”包装成“基于量子不确定性原理的深度观察”。</p>
          <button class="bg-black text-white font-black py-3 rounded-xl hover:bg-pink-500 transition-colors">立即下载 (1KB)</button>
        </div>

        <div class="neo-card bg-mint p-8 rounded-[2rem] flex flex-col group rotate-[1deg]">
          <div class="h-48 bg-white rounded-2xl mb-6 flex items-center justify-center border-2 border-black group-hover:rotate-3 transition-transform">
            <Icon class="text-black text-8xl" icon="mdi:tools"></Icon>
          </div>
          <h3 class="text-3xl font-black mb-4">逻辑谬误检测器</h3>
          <p class="text-lg font-bold text-slate-800 mb-6 flex-grow">其实只是一个随机生成“你这就是稻草人谬误”文字的网页，但非常好用。</p>
          <button class="bg-black text-white font-black py-3 rounded-xl hover:bg-blue-500 transition-colors">在线使用 (有点卡)</button>
        </div>

        <div class="neo-card bg-blue-400 p-8 rounded-[2rem] flex flex-col group rotate-[-1deg]">
          <div class="h-48 bg-yellow-100 rounded-2xl mb-6 flex items-center justify-center border-2 border-black">
            <Icon class="text-yellow-600 text-8xl" icon="mdi:coffee-to-go"></Icon>
          </div>
          <h3 class="text-3xl font-black mb-4">无限续杯奶茶优惠券</h3>
          <p class="text-lg font-bold text-white mb-6 flex-grow">专为深夜辩论准备。虽然不能真的买奶茶，但看着它能产生心理上的饱腹感。</p>
          <button class="bg-black text-white font-black py-3 rounded-xl hover:bg-yellow-400 hover:text-black transition-colors">凭空领取</button>
        </div>

        <div class="neo-card bg-purple-400 p-8 rounded-[2rem] flex flex-col group">
          <div class="h-48 bg-white rounded-2xl mb-6 flex items-center justify-center border-2 border-black">
            <Icon class="text-purple-500 text-8xl" icon="mdi:account-voice"></Icon>
          </div>
          <h3 class="text-3xl font-black mb-4">专业背景音效包</h3>
          <p class="text-lg font-bold text-white mb-6 flex-grow">包含“哦？”、“真的吗？”以及“我不能理解”三种高频辩论语气词。</p>
          <button class="bg-white text-black font-black py-3 rounded-xl border-4 border-black shadow-[4px_4px_0px_black] active:shadow-none">点击试听</button>
        </div>

        <div class="neo-card bg-white p-8 rounded-[2rem] flex flex-col group rotate-[2deg]">
          <div class="h-48 bg-slate-100 rounded-2xl mb-6 flex items-center justify-center border-2 border-black">
            <Icon class="text-black text-8xl" icon="mdi:file-certificate"></Icon>
          </div>
          <h3 class="text-3xl font-black mb-4">空白“认怂”证明书</h3>
          <p class="text-lg font-bold text-slate-500 mb-6 flex-grow">当遇到不可理喻的对手时，打印此证并送给他，能有效保护自己的脑细胞。</p>
          <button class="bg-black text-white font-black py-3 rounded-xl hover:bg-red-500 transition-colors">PDF 下载 (慎用)</button>
        </div>
      </div>

      <div class="mt-24 text-center neo-card p-16 rounded-[4rem] bg-white">
        <h3 class="text-4xl font-black mb-6 humor-font">还没看够？</h3>
        <p class="text-2xl font-bold mb-8 text-slate-500">别急，我们的资源就像你的逻辑漏洞一样多，正在不断添加中...</p>
        <div class="flex justify-center gap-6">
          <RouterLink class="bg-pink-500 text-white font-black px-10 py-4 rounded-2xl border-4 border-black hover:bg-pink-600" to="/blog">去博客看看</RouterLink>
          <RouterLink class="bg-black text-white font-black px-10 py-4 rounded-2xl border-4 border-black hover:bg-slate-800" to="/">回首页补魔</RouterLink>
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
import { RouterLink } from 'vue-router'
import FloatingNav from '../components/layout/FloatingNav.vue'
import MainNav from '../components/layout/MainNav.vue'
</script>

<style>
.neo-card {
  background: white;
  border: 4px solid black;
  box-shadow: 10px 10px 0px black;
  transition: all 0.3s;
}

.neo-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 15px 15px 0px black;
}
</style>
