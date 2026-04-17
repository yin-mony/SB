<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <main class="relative z-10 max-w-4xl mx-auto px-6 py-20">
      <header class="text-center mb-16">
        <h2 class="text-6xl humor-font font-black mb-4">
          十万个 <span class="bg-blue-500 text-white px-4 border-4 border-black inline-block rotate-[-2deg]">为什么</span>
        </h2>
        <p class="text-xl font-bold text-slate-500">（虽然我们不保证答案一定正确，但我们保证它们一定很有趣）</p>
      </header>

      <div class="space-y-12">
        <div class="faq-item faq-card bg-white p-8 rounded-3xl relative">
          <Icon
            class="absolute -top-6 -left-6 text-pink-500 text-6xl rotate-[-15deg] drop-shadow-[2px_2px_0px_black]"
            icon="mdi:help-circle"
          ></Icon>
          <h3 class="text-2xl font-black mb-4 text-black">Q: 为什么我在这里总是辩论失败？</h3>
          <div class="bg-slate-50 p-6 rounded-2xl border-2 border-dashed border-slate-300">
            <p class="font-bold text-lg">
              A:
              可能是因为你的对手是一台由于某种原因获得自主意识的旧电冰箱，或者是因为你太讲道理了。在这里，道理只是佐料，有趣才是主菜。建议尝试在论证中加入“我昨晚梦见的”作为证据。
            </p>
          </div>
        </div>

        <div class="faq-item faq-card bg-yellow-400 p-8 rounded-3xl relative rotate-[1deg]">
          <h3 class="text-2xl font-black mb-4 text-black">Q: 我可以带我的狗一起来参加辩论吗？</h3>
          <div class="bg-white p-6 rounded-2xl border-4 border-black">
            <p class="font-bold text-lg text-slate-800">
              A:
              当然可以！事实上，我们这里有 15% 的高质量论点是由金毛寻回犬通过乱踩键盘生成的。如果你的狗能通过“汪”来表达对算法偏见的看法，我们将授予它“荣誉院士”称号。
            </p>
          </div>
        </div>

        <div class="faq-item faq-card bg-mint p-8 rounded-3xl relative rotate-[-1deg]">
          <h3 class="text-2xl font-black mb-4 text-black">Q: 这里的积分可以换钱吗？</h3>
          <div class="bg-black text-white p-6 rounded-2xl">
            <p class="font-bold text-lg">
              A:
              不可以换钱，但可以换取内心的虚荣和对他人的降维打击。此外，积分达到 100 万的用户可以获得一次让管理员对着月亮喊你名字的机会（虽然我们不一定会真的去做）。
            </p>
          </div>
        </div>

        <div class="faq-item faq-card bg-purple-500 p-8 rounded-3xl relative">
          <h3 class="text-2xl font-black mb-4 text-white">Q: 如果我吵架吵哭了怎么办？</h3>
          <div class="bg-white p-6 rounded-2xl border-4 border-black">
            <p class="font-bold text-lg text-slate-800">
              A:
              请立即去喝一杯奶茶。我们社区的口号是：辩论诚可贵，奶茶价更高。如果你真的哭了，我们可以帮你给对手发送一个带有“你太坏了”字样的幽灵图标。
            </p>
          </div>
        </div>

        <div class="faq-item faq-card bg-white p-8 rounded-3xl relative rotate-[0.5deg]">
          <h3 class="text-2xl font-black mb-4 text-black">Q: 这里会有相亲环节吗？</h3>
          <div class="bg-pink-100 p-6 rounded-2xl border-4 border-black border-dotted">
            <p class="font-bold text-lg text-slate-700">
              A:
              任何辩论平台最终都会变成相亲平台。如果你发现有人和你对“波粒二象性对哲学的影响”有相同见解，那就赶紧私信吧。但请记住：辩论场上的爱，往往始于三观契合，终于谁洗碗。
            </p>
          </div>
        </div>
      </div>

      <div class="mt-20 text-center bg-black p-10 rounded-[3rem] text-white">
        <h3 class="text-3xl font-black mb-4">还有更多奇葩问题？</h3>
        <p class="text-slate-400 mb-8">别憋着，憋坏了我们不负责。快去社区发帖吧！</p>
        <RouterLink
          class="inline-block bg-yellow-400 text-black px-12 py-4 rounded-2xl font-black text-2xl border-4 border-black hover:scale-110 transition-transform"
          to="/debate-list?create=1"
        >
          我也要问！
        </RouterLink>
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
.faq-card {
  background: white;
  border: 4px solid black;
  box-shadow: 10px 10px 0px black;
  transition: all 0.3s;
}

.faq-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 14px 14px 0px black;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(-2deg);
}
</style>
