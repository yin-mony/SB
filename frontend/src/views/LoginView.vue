<template>
  <div class="flex items-center justify-center min-h-screen p-6">
    <div class="flash-bg"></div>
    <div class="login-card bg-white max-w-md w-full p-10 rounded-[60px] relative">
      <div
        class="absolute -top-12 -left-12 bg-yellow-400 border-4 border-black p-4 rounded-2xl rotate-[-12deg] shadow-[8px_8px_0px_black] hidden md:block"
      >
        <Icon class="text-black" icon="mdi:lightning-bolt" width="48"></Icon>
      </div>
      <div
        class="absolute -bottom-10 -right-10 bg-pink-500 border-4 border-black p-4 rounded-full rotate-[15deg] shadow-[8px_8px_0px_black] hidden md:block"
      >
        <Icon class="text-white" icon="mdi:ufo-outline" width="48"></Icon>
      </div>

      <div class="text-center mb-10">
        <h1 class="text-5xl humor-font font-black mb-4">🔑 闪现进入</h1>
        <p class="font-bold text-slate-500">验证你的灵魂深度，或者随便填个名字。</p>
      </div>

      <form class="space-y-6" @submit.prevent="submit">
        <div class="input-group">
          <label class="block font-black text-lg mb-2">用户名（或历史绑定邮箱）</label>
          <input
            v-model="account"
            class="w-full px-6 py-4 rounded-2xl font-bold text-lg"
            placeholder="比如：精神小伙、熬夜冠军..."
            required
            type="text"
          />
        </div>
        <div class="input-group">
          <label class="block font-black text-lg mb-2">接头暗号 (密码)</label>
          <input
            v-model="password"
            class="w-full px-6 py-4 rounded-2xl font-bold text-lg"
            placeholder="别写 123456，太没创意了"
            required
            type="password"
          />
        </div>
        <div class="flex items-center justify-between font-black text-sm">
          <label class="flex items-center gap-2 cursor-pointer">
            <input v-model="rememberMe" class="w-5 h-5 border-4 border-black rounded shadow-none accent-pink-500" type="checkbox" />
            记住我 (免得下次闪现失败)
          </label>
          <RouterLink class="text-pink-600 hover:underline" :to="{ path: '/forgot-password', query: { redirect: route.query.redirect } }">
            忘记暗号了？
          </RouterLink>
        </div>
        <div v-if="errorMsg" class="bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
          {{ errorMsg }}
        </div>
        <button
          class="w-full bg-black text-white py-5 rounded-3xl text-2xl font-black bouncy-btn shadow-[10px_10px_0px_#ff477e] shake mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="loading"
          type="submit"
        >
          🚀 立即闪现！
        </button>
        <div class="text-center mt-8 pt-6 border-t-4 border-black border-dashed">
          <p class="font-bold">
            还没有通行证？
            <RouterLink class="text-accent underline font-black" to="/register">去整一个</RouterLink>
          </p>
          <button class="mt-4 text-slate-400 font-bold hover:text-black transition-colors" type="button" @click="goHome">先随便逛逛 (怂了？)</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const account = ref('')
const password = ref('')
const rememberMe = ref(true)
const loading = ref(false)
const errorMsg = ref('')

const normalizeRedirect = (v) => {
  if (Array.isArray(v)) v = v[0]
  if (typeof v !== 'string') return ''
  const s = v.trim()
  if (!s) return ''
  if (!s.startsWith('/')) return ''
  if (s.startsWith('//')) return ''
  if (s.startsWith('/login') || s.startsWith('/register')) return ''
  return s
}

const submit = async () => {
  errorMsg.value = ''
  loading.value = true
  try {
    await auth.login({ account: account.value, password: password.value, rememberMe: rememberMe.value })
    await auth.fetchProfile().catch(() => {})
    const redirect = normalizeRedirect(route.query.redirect) || normalizeRedirect(sessionStorage.getItem('last_path')) || '/profile'
    router.replace(redirect)
  } catch (e) {
    errorMsg.value = e?.message || '登录失败'
  } finally {
    loading.value = false
  }
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
  animation: flashIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  border: 8px solid black;
  box-shadow: 20px 20px 0px black;
}

@keyframes flashIn {
  0% {
    transform: scale(0.5) rotate(-20deg);
    opacity: 0;
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

.input-group input {
  border: 4px solid black;
  transition: all 0.2s;
}

.input-group input:focus {
  transform: translate(-4px, -4px);
  box-shadow: 8px 8px 0px black;
  outline: none;
  background-color: #fff9e6;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(-2deg);
}

.shake:hover {
  animation: shake 0.5s infinite;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px) rotate(-1deg);
  }
  75% {
    transform: translateX(5px) rotate(1deg);
  }
}
</style>
