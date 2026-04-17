<template>
  <div class="flex items-center justify-center min-h-screen p-6">
    <div class="flash-bg"></div>
    <div class="register-card bg-white max-w-lg w-full p-10 rounded-[60px] relative">
      <div class="absolute -top-12 -right-12 bg-accent border-4 border-black p-4 rounded-full rotate-[12deg] shadow-[8px_8px_0px_black] hidden md:block">
        <Icon class="text-white" icon="mdi:robot-happy-outline" width="48"></Icon>
      </div>
      <div
        class="absolute -bottom-10 -left-10 bg-yellow-400 border-4 border-black p-4 rounded-2xl rotate-[-15deg] shadow-[8px_8px_0px_black] hidden md:block text-black"
      >
        <span class="font-black text-xl">真能写？</span>
      </div>

      <div class="text-center mb-8">
        <h1 class="text-5xl humor-font font-black mb-4">👽 整一个通行证</h1>
        <p class="font-bold text-slate-500">只要<strong>用户名 + 图片验证码</strong>，再设个暗号就能进来。</p>
      </div>

      <form class="space-y-4" @submit.prevent="submit">
        <div class="input-group">
          <label class="block font-black text-sm mb-1 ml-2">用户名</label>
          <input v-model="username" class="w-full px-4 py-3 rounded-xl font-bold" placeholder="张三、李四、隔壁老王..." required type="text" autocomplete="username" />
        </div>
        <div class="input-group">
          <label class="block font-black text-sm mb-1 ml-2">图片验证码</label>
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-3">
            <input
              v-model="captcha"
              class="w-full min-w-0 flex-1 px-4 py-3 rounded-xl font-bold tracking-widest sm:max-w-xs"
              placeholder="请输入图中的字符"
              maxlength="10"
              required
              type="text"
              autocomplete="off"
            />
            <div class="flex items-center gap-3 w-full sm:w-auto sm:shrink-0 justify-between sm:justify-start">
              <img
                v-if="captchaImage"
                :src="captchaImage"
                alt="captcha"
                class="box-border h-[52px] w-[140px] shrink-0 border-4 border-black rounded-xl bg-white object-contain select-none"
              />
              <button
                type="button"
                class="shrink-0 box-border h-[52px] min-w-[5.5rem] px-3 flex items-center justify-center bg-white border-4 border-black rounded-xl text-sm font-black bouncy-btn hover:bg-yellow-200 disabled:opacity-50"
                :disabled="captchaLoading"
                @click="refreshCaptcha"
              >
                {{ captchaLoading ? '刷新中…' : '换一张' }}
              </button>
            </div>
          </div>
        </div>
        <div class="input-group">
          <label class="block font-black text-sm mb-1 ml-2">接头暗号 (设个难点的)</label>
          <input v-model="password" class="w-full px-4 py-4 rounded-xl font-bold" placeholder="建议混入几个乱码..." required type="password" autocomplete="new-password" />
        </div>
        <div class="input-group">
          <label class="block font-black text-sm mb-1 ml-2">再次确认暗号 (别手抖)</label>
          <input v-model="password2" class="w-full px-4 py-4 rounded-xl font-bold" placeholder="手抖了我也没法救你" required type="password" autocomplete="new-password" />
        </div>
        <div v-if="errorMsg" class="bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
          {{ errorMsg }}
        </div>
        <label class="flex items-center gap-2 font-black text-sm ml-1 cursor-pointer">
          <input v-model="rememberMe" class="w-4 h-4 border-4 border-black rounded accent-pink-500" type="checkbox" />
          在本机记住登录（关闭浏览器后是否仍保持登录，取决于此项）
        </label>
        <button
          class="w-full mt-4 py-5 rounded-[28px] text-2xl font-black border-4 border-black shadow-[10px_10px_0px_black] bouncy-btn disabled:opacity-50 disabled:cursor-not-allowed bg-gradient-to-r from-pink-500 via-accent to-blue-500 text-white hover:shadow-[14px_14px_0px_black] hover:-translate-y-1 transition-all"
          :disabled="loading"
          type="submit"
        >
          {{ loading ? '注册中…' : '✅ 领证出发！' }}
        </button>
        <div class="text-center mt-6 pt-4 border-t-4 border-black border-dashed">
          <p class="font-bold">
            已经有证了？
            <RouterLink class="text-pink-600 underline font-black" to="/login">直接闪现</RouterLink>
          </p>
          <button class="mt-4 text-slate-400 font-bold hover:text-black transition-colors" type="button" @click="goHome">先随便逛逛 (不想注册？)</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { http } from '../api/http'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const username = ref('')
const captcha = ref('')
const captchaId = ref('')
const captchaImage = ref('')
const captchaLoading = ref(false)
const password = ref('')
const password2 = ref('')
const rememberMe = ref(true)
const loading = ref(false)
const errorMsg = ref('')

const refreshCaptcha = async () => {
  captchaLoading.value = true
  try {
    const r = await http.post('auth/captcha/', { purpose: 'register' })
    captchaId.value = r?.captcha_id || ''
    captchaImage.value = r?.image || ''
  } catch (e) {
    errorMsg.value = e?.message || '验证码加载失败'
  } finally {
    captchaLoading.value = false
  }
}

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
  if (password.value !== password2.value) {
    errorMsg.value = '两次密码不一致'
    return
  }
  if (!captcha.value.trim()) {
    errorMsg.value = '请填写图片验证码'
    return
  }
  if (!captchaId.value) {
    await refreshCaptcha()
    if (!captchaId.value) return
  }
  loading.value = true
  try {
    await auth.register(
      {
        username: username.value.trim(),
        password: password.value,
        captcha_id: captchaId.value,
        captcha: captcha.value.trim()
      },
      { rememberMe: rememberMe.value }
    )
    await auth.fetchProfile().catch(() => {})
    const redirect = normalizeRedirect(route.query.redirect) || normalizeRedirect(sessionStorage.getItem('last_path')) || '/profile'
    router.replace(redirect)
  } catch (e) {
    errorMsg.value = e?.message || '注册失败'
  } finally {
    loading.value = false
  }
}

const goHome = () => {
  router.push('/')
}

onMounted(() => {
  document.body.classList.add('overflow-hidden')
  refreshCaptcha()
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
  background: linear-gradient(135deg, #8338ec, #3a86ff, #06d6a0);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite alternate;
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

.register-card {
  animation: flashIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  border: 8px solid black;
  box-shadow: -20px 20px 0px black;
}

@keyframes flashIn {
  0% {
    transform: scale(0.5) rotate(20deg);
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
  transform: translate(4px, -4px);
  box-shadow: -8px 8px 0px black;
  outline: none;
  background-color: #f0fff4;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(2deg);
}

.wiggle:hover {
  animation: wiggle 0.5s infinite;
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
