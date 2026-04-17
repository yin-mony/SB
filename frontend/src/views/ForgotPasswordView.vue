<template>
  <div class="flex items-center justify-center min-h-screen p-6">
    <div class="flash-bg"></div>
    <div class="login-card bg-white max-w-md w-full p-10 rounded-[60px] relative">
      <div class="text-center mb-10">
        <h1 class="text-5xl humor-font font-black mb-4">🧩 找回暗号</h1>
        <p class="font-bold text-slate-500">输入<strong>用户名</strong>，去「重置暗号」页完成验证与重置。</p>
      </div>

      <form class="space-y-6" @submit.prevent="goReset">
        <div class="input-group">
          <label class="block font-black text-lg mb-2">用户名</label>
          <input
            v-model="username"
            class="w-full px-6 py-4 rounded-2xl font-bold text-lg"
            placeholder="注册时用的用户名"
            required
            type="text"
            autocomplete="username"
          />
        </div>

        <div v-if="errorMsg" class="bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
          {{ errorMsg }}
        </div>

        <button
          class="w-full bg-black text-white py-5 rounded-3xl text-2xl font-black bouncy-btn shadow-[10px_10px_0px_#ff477e] shake mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="loading || !username.trim()"
          type="submit"
        >
          去重置暗号
        </button>

        <div class="text-center mt-8 pt-6 border-t-4 border-black border-dashed">
          <p class="font-bold">
            想起来了？
            <RouterLink class="text-accent underline font-black" :to="{ path: '/login', query: { redirect } }">回去登录</RouterLink>
          </p>
          <button class="mt-4 text-slate-400 font-bold hover:text-black transition-colors" type="button" @click="goHome">先随便逛逛</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

const username = ref('')
const loading = ref(false)
const errorMsg = ref('')

const redirect = computed(() => {
  const v = route.query.redirect
  if (Array.isArray(v)) return v[0] || ''
  return typeof v === 'string' ? v : ''
})

const goReset = () => {
  router.push({
    path: '/reset-password',
    query: { username: username.value.trim(), redirect: redirect.value || undefined }
  })
}

const goHome = () => {
  router.push('/')
}

onMounted(() => {
  document.body.classList.add('overflow-hidden')
})

onUnmounted(() => {
  document.body.classList.remove('overflow-hidden')
})
</script>

<style>
.flash-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: linear-gradient(45deg, #ff477e, #ffbe0b, #3a86ff, #06d6a0);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.login-card {
  border: 6px solid black;
  box-shadow: 12px 12px 0px black;
}

.input-group input {
  border: 4px solid black;
  background: #f8fafc;
  transition: all 0.2s ease;
}

.input-group input:focus {
  outline: none;
  transform: translateY(-2px);
  box-shadow: 6px 6px 0px black;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(-2deg);
}
</style>
