<template>
  <div class="flex items-center justify-center min-h-screen p-6">
    <div class="flash-bg"></div>
    <div class="login-card bg-white max-w-md w-full p-10 rounded-[60px] relative">
      <div class="text-center mb-10">
        <h1 class="text-5xl humor-font font-black mb-4">🔁 重置暗号</h1>
        <p class="font-bold text-slate-500">输入用户名、图片验证码和新密码。</p>
      </div>

      <form class="space-y-6" @submit.prevent="submit">
        <div class="input-group">
          <label class="block font-black text-lg mb-2">用户名</label>
          <input
            v-model="username"
            class="w-full px-6 py-4 rounded-2xl font-bold text-lg"
            placeholder="与找回页一致"
            required
            type="text"
            autocomplete="username"
          />
        </div>
        <div class="input-group">
          <label class="block font-black text-lg mb-2">图片验证码</label>
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-3">
            <input
              v-model="captcha"
              class="w-full min-w-0 flex-1 px-6 py-4 rounded-2xl font-bold text-lg tracking-widest sm:max-w-xs"
              placeholder="输入图中字符"
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
                class="shrink-0 box-border h-[52px] min-w-[5.5rem] px-3 flex items-center justify-center bg-white border-4 border-black rounded-xl font-black bouncy-btn hover:bg-yellow-200 disabled:opacity-50"
                :disabled="captchaLoading"
                @click="refreshCaptcha"
              >
                {{ captchaLoading ? '刷新中…' : '换一张' }}
              </button>
            </div>
          </div>
        </div>
        <div class="input-group">
          <label class="block font-black text-lg mb-2">新暗号</label>
          <input
            v-model="password"
            class="w-full px-6 py-4 rounded-2xl font-bold text-lg"
            placeholder="至少 6 位"
            required
            type="password"
            autocomplete="new-password"
          />
        </div>
        <div class="input-group">
          <label class="block font-black text-lg mb-2">再输一遍</label>
          <input
            v-model="password2"
            class="w-full px-6 py-4 rounded-2xl font-bold text-lg"
            placeholder="确认一下"
            required
            type="password"
            autocomplete="new-password"
          />
        </div>

        <div v-if="errorMsg" class="bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
          {{ errorMsg }}
        </div>
        <div v-if="successMsg" class="bg-green-100 border-4 border-black p-4 rounded-2xl font-black text-green-800">
          {{ successMsg }}
        </div>

        <button
          class="w-full bg-black text-white py-5 rounded-3xl text-2xl font-black bouncy-btn shadow-[10px_10px_0px_#ff477e] shake mt-4 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="loading"
          type="submit"
        >
          ✅ 立即重置
        </button>

        <div class="text-center mt-8 pt-6 border-t-4 border-black border-dashed">
          <p class="font-bold">
            重置完了？
            <RouterLink class="text-accent underline font-black" :to="{ path: '/login', query: { redirect } }">回去登录</RouterLink>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { http } from '../api/http'

const router = useRouter()
const route = useRoute()

const username = ref('')
const captchaId = ref('')
const captcha = ref('')
const captchaImage = ref('')
const captchaLoading = ref(false)
const password = ref('')
const password2 = ref('')
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const redirect = computed(() => {
  const v = route.query.redirect
  if (Array.isArray(v)) return v[0] || ''
  return typeof v === 'string' ? v : ''
})

watch(
  () => route.query.username,
  (v) => {
    const u = Array.isArray(v) ? v[0] : typeof v === 'string' ? v : ''
    if (u) username.value = u
  },
  { immediate: true }
)

const submit = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  if (password.value !== password2.value) {
    errorMsg.value = '两次输入不一致'
    return
  }
  if (!username.value.trim()) {
    errorMsg.value = '请填写用户名'
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
    await http.post('auth/password-reset/confirm/', {
      username: username.value.trim(),
      captcha_id: captchaId.value,
      captcha: captcha.value.trim(),
      new_password: password.value
    })
    successMsg.value = '重置成功，现在可以去登录了。'
    setTimeout(() => {
      router.replace({ path: '/login', query: { redirect: redirect.value || undefined } })
    }, 600)
  } catch (e) {
    errorMsg.value = e?.message || '重置失败'
  } finally {
    loading.value = false
  }
}

const refreshCaptcha = async () => {
  captchaLoading.value = true
  try {
    const r = await http.post('auth/captcha/', { purpose: 'password_reset' })
    captchaId.value = r?.captcha_id || ''
    captchaImage.value = r?.image || ''
  } catch (e) {
    errorMsg.value = e?.message || '验证码加载失败'
  } finally {
    captchaLoading.value = false
  }
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
