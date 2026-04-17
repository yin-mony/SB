<template>
  <nav class="sticky top-0 z-50 bg-white/70 backdrop-blur-xl border-b-4 border-black">
    <div class="max-w-7xl mx-auto px-6 h-24 flex items-center justify-between">
      <RouterLink class="flex items-center space-x-3 cursor-pointer group" to="/">
        <div
          class="bg-pink-500 p-2 rounded-2xl text-white transform group-hover:rotate-12 transition-transform shadow-[4px_4px_0px_black]"
        >
          <Icon icon="mdi:emoticon-tongue-outline" width="40" />
        </div>
        <div>
          <h1 class="text-3xl humor-font font-bold tracking-tight text-black">思辩乐园</h1>
          <p class="text-[10px] uppercase tracking-widest text-pink-600 font-black">Debate Paradise &amp; Chill</p>
        </div>
      </RouterLink>

      <div class="hidden lg:flex items-center space-x-8">
        <RouterLink :class="navClass('/')" to="/">🍟 首页</RouterLink>
        <RouterLink :class="navClass('/debate-list')" to="/debate-list">🤼 话题池</RouterLink>
        <RouterLink :class="navClass('/blog')" to="/blog">📝 胡说</RouterLink>
        <RouterLink :class="navClass('/faq')" to="/faq">❓ 问答</RouterLink>
        <div class="h-8 w-[4px] bg-black"></div>
        <RouterLink
          v-if="!auth.isAuthed"
          class="bg-yellow-400 border-4 border-black text-black font-black px-8 py-3 rounded-full bouncy-btn shadow-[6px_6px_0px_black] active:translate-y-1 active:shadow-none"
          to="/login"
        >
          🔑 闪现进入
        </RouterLink>
        <RouterLink
          v-else
          class="bg-black border-4 border-black text-white font-black px-6 py-3 rounded-full bouncy-btn shadow-[6px_6px_0px_black] active:translate-y-1 active:shadow-none flex items-center gap-3"
          to="/profile"
        >
          <img class="w-8 h-8 rounded-full border-2 border-white" :src="avatarUrl" alt="avatar" />
          <span class="truncate max-w-[140px]">个人中心</span>
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const auth = useAuthStore()
const currentPath = computed(() => route.path)
const avatarUrl = computed(
  () => auth.user?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(auth.user?.username || 'user')}`
)

const navClass = (path) => {
  const cur = currentPath.value
  let active = cur === path
  if (!active && path === '/blog' && (cur === '/blog' || cur.startsWith('/blog-'))) active = true
  if (!active && path === '/debate-list' && (cur === '/debate-list' || cur === '/debate-detail')) active = true
  return [
    'nav-link',
    'text-lg',
    'font-black',
    active ? 'text-pink-600 border-b-4 border-pink-500' : 'text-black'
  ].join(' ')
}
</script>
