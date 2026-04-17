<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <header class="bg-purple-600 py-16 text-white text-center relative overflow-hidden border-b-4 border-black">
      <div class="abstract-dot bg-yellow-300 w-40 h-40 -top-10 -left-10"></div>
      <div class="max-w-7xl mx-auto px-6 relative z-10">
        <h1 class="text-6xl humor-font font-black mb-6">🤼 话题池</h1>
        <p class="text-xl font-bold mb-10">
          这里是逻辑的角斗场，也是脑洞的培养皿。<br />
          如果你觉得某个话题太正常，那一定是你还没看评论区。
        </p>
        <button
          class="bg-mint text-black text-3xl font-black px-12 py-6 rounded-3xl bouncy-btn border-4 border-black shadow-[10px_10px_0px_black] hover:-rotate-2"
          type="button"
          @click="openCreate"
        >
          🎤 我要发起话题！
        </button>
      </div>
    </header>

    <section class="bg-white border-b-4 border-black sticky top-20 z-40 py-4">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row gap-6 items-center justify-between">
        <div class="relative w-full md:w-[450px]">
          <Icon class="absolute left-4 top-1/2 -translate-y-1/2 text-pink-500" icon="mdi:duck" width="28"></Icon>
          <input
            v-model="queryText"
            class="w-full pl-14 pr-4 py-4 bg-yellow-50 border-4 border-black rounded-2xl focus:outline-none focus:ring-4 focus:ring-pink-400/30 text-xl font-bold placeholder:text-slate-400"
            placeholder="搜搜看谁在讲歪理..."
            type="text"
          />
        </div>
        <div class="flex items-center gap-4 overflow-x-auto w-full md:w-auto pb-2 md:pb-0">
          <button :class="filterBtnClass('')" type="button" @click="setCategory('')">全部都要</button>
          <button
            v-for="c in categories"
            :key="c.category"
            :class="filterBtnClass(c.category, 'hover:bg-yellow-300')"
            type="button"
            @click="setCategory(c.category)"
          >
            <span>{{ c.category }}</span>
            <span class="ml-2 inline-flex items-center justify-center min-w-7 h-7 px-2 bg-black/10 border-2 border-black rounded-full text-[10px] font-black">
              {{ c.count }}
            </span>
          </button>
        </div>
      </div>
    </section>

    <main class="max-w-7xl mx-auto px-6 py-16">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-10">
        <div v-if="topicsError" class="w-full md:flex-1 bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
          {{ topicsError }}
          <button class="ml-3 underline" type="button" @click="reload">重试</button>
        </div>
        <div v-else class="w-full md:flex-1 text-sm font-black text-slate-500">
          <span v-if="loadingTopics">加载中...</span>
          <span v-else>共 {{ topics.length }} 条（第 {{ page }} 页）</span>
        </div>

        <div class="flex items-center gap-3 w-full md:w-auto justify-end">
          <button
            :class="sortBtnClass('hot')"
            type="button"
            @click="setSort('hot')"
          >
            🔥 热门
          </button>
          <button
            :class="sortBtnClass('new')"
            type="button"
            @click="setSort('new')"
          >
            🕒 最新
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
        <RouterLink
          v-for="(t, idx) in topics"
          :key="t.id"
          v-reveal="idx * 50"
          :class="['neo-card rounded-3xl overflow-hidden flex flex-col group cursor-pointer', idx % 3 === 1 ? 'bg-blue-100/40' : idx % 3 === 2 ? 'bg-yellow-50' : '']"
          :to="{ path: '/debate-detail', query: { id: String(t.id) } }"
        >
          <div class="p-8 flex-1">
            <div class="flex items-center justify-between mb-6">
              <span :class="['px-4 py-1 border-2 border-black rounded-full text-xs font-black uppercase tracking-widest category-pill', categoryPillBg(idx)]">
                # {{ t.category }}
              </span>
              <span class="text-xs font-black text-slate-500">🔥 热度：{{ Math.round(t.hot_score || 0) }}</span>
            </div>
            <h3 class="text-3xl font-black mb-4 leading-snug group-hover:text-pink-600 transition-colors">
              {{ t.title }}
            </h3>
            <p class="text-slate-600 font-bold mb-6 line-clamp-3">
              {{ t.description }}
            </p>
            <div class="space-y-4 mb-8">
              <div class="flex items-center gap-3">
                <div class="w-4 h-4 rounded-full bg-purple-500 border-2 border-black"></div>
                <span class="text-sm font-bold">正方: {{ t.side_a_name }}</span>
              </div>
              <div class="flex items-center gap-3">
                <div class="w-4 h-4 rounded-full bg-pink-500 border-2 border-black"></div>
                <span class="text-sm font-bold">反方: {{ t.side_b_name }}</span>
              </div>
            </div>
            <div class="pt-6 border-t-2 border-dashed border-black flex items-center justify-between">
              <div class="text-xs font-black px-2 py-1 bg-pink-100 border border-black">状态: {{ t.status }}</div>
              <div class="flex items-center gap-4 text-xs font-black">
                <span class="flex items-center gap-1"><Icon icon="mdi:message-outline" width="18"></Icon> {{ t.comment_count || 0 }}</span>
                <span class="flex items-center gap-1"><Icon icon="mdi:eye-outline" width="18"></Icon> {{ toK(t.view_count || 0) }}</span>
              </div>
            </div>
          </div>
          <div class="bg-black p-4 text-center">
            <span class="text-white font-black text-lg hover:text-mint transition-colors">🍔 咬一口话题</span>
          </div>
        </RouterLink>

        <div
          v-if="!topics.length && !loadingTopics && !topicsError"
          class="neo-card rounded-3xl overflow-hidden flex flex-col border-dashed bg-transparent shadow-none items-center justify-center min-h-[240px] md:col-span-2 lg:col-span-3"
        >
          <div class="text-center p-10">
            <p class="text-3xl humor-font font-black text-black mb-4">空空如也</p>
            <p class="text-slate-500 font-bold mb-8">没找到符合条件的话题。要不你来开一个？</p>
            <button class="bg-black text-white px-8 py-4 rounded-2xl font-black border-4 border-black shadow-[8px_8px_0px_black] bouncy-btn" type="button" @click="openCreate">
              🎤 我来发起
            </button>
          </div>
        </div>

        <div
          class="neo-card rounded-3xl overflow-hidden flex flex-col group border-dashed bg-transparent shadow-none hover:shadow-[8px_8px_0px_black] hover:bg-white transition-all items-center justify-center min-h-[400px] cursor-pointer"
          @click="openCreate"
        >
          <div class="text-center p-8">
            <div
              class="w-20 h-20 bg-yellow-400 border-4 border-black rounded-full flex items-center justify-center text-black bouncy-btn shadow-[6px_6px_0px_black] mb-6 mx-auto"
            >
              <Icon icon="mdi:plus" width="40"></Icon>
            </div>
            <p class="text-3xl humor-font font-black text-black">我想开个脑洞</p>
            <p class="text-slate-500 font-bold mt-4">无需审核，只要够抽象！</p>
          </div>
        </div>
      </div>

      <div class="mt-24 flex items-center justify-center gap-4">
        <button
          :disabled="page <= 1 || loadingTopics"
          class="w-14 h-14 border-4 border-black bg-white rounded-2xl flex items-center justify-center hover:bg-pink-500 hover:text-white transition-all shadow-[4px_4px_0px_black] active:translate-y-1 active:shadow-none font-black text-2xl"
          type="button"
          @click="goPage(page - 1)"
        >
          <Icon icon="mdi:chevron-left"></Icon>
        </button>
        <button
          class="w-14 h-14 border-4 border-black bg-yellow-400 rounded-2xl flex items-center justify-center font-black text-2xl shadow-[4px_4px_0px_black]"
          type="button"
          @click="goPage(page)"
        >
          {{ page }}
        </button>
        <button
          :disabled="!hasMore || loadingTopics"
          class="w-14 h-14 border-4 border-black bg-white rounded-2xl flex items-center justify-center hover:bg-pink-500 hover:text-white transition-all shadow-[4px_4px_0px_black] active:translate-y-1 active:shadow-none font-black text-2xl"
          type="button"
          @click="goPage(page + 1)"
        >
          <Icon icon="mdi:chevron-right"></Icon>
        </button>
      </div>
    </main>

    <div v-show="createModalOpen" class="fixed inset-0 z-[200] flex items-center justify-center p-6 bg-black/80 backdrop-blur-sm">
      <div class="bg-white border-8 border-black w-full max-w-2xl rounded-[60px] p-10 modal-enter overflow-y-auto max-h-[90vh]">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-4xl humor-font font-black">🎤 开启一段新的抬杠</h2>
          <button
            class="w-12 h-12 border-4 border-black rounded-full flex items-center justify-center hover:bg-red-500 hover:text-white transition-colors"
            type="button"
            @click="closeCreate"
          >
            <Icon icon="mdi:close" width="30"></Icon>
          </button>
        </div>
        <form class="space-y-6" @submit.prevent="submitCreate">
          <div>
            <label class="block font-black mb-2 ml-4 text-xl">话题名称 (足够离谱吗？)</label>
            <input
              v-model="createForm.title"
              class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50 focus:outline-none"
              placeholder="比如：咸豆腐脑是否应该被定为非法？"
              required
              type="text"
            />
            <p v-if="createErrors.title" class="mt-2 ml-4 text-sm font-black text-red-600">{{ createErrors.title }}</p>
          </div>
          <div>
            <label class="block font-black mb-2 ml-4 text-xl">话题描述 (骗更多人进来吵架)</label>
            <textarea
              v-model="createForm.description"
              class="w-full p-6 border-4 border-black rounded-3xl font-bold bg-slate-50 focus:outline-none h-32"
              placeholder="描述一下这个话题的冲突点..."
              required
            ></textarea>
            <p v-if="createErrors.description" class="mt-2 ml-4 text-sm font-black text-red-600">{{ createErrors.description }}</p>
          </div>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block font-black mb-2 ml-4">正方立场</label>
              <input v-model="createForm.side_a_name" class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50" placeholder="比如：美味即正义" type="text" />
              <p v-if="createErrors.side_a_name" class="mt-2 ml-4 text-sm font-black text-red-600">{{ createErrors.side_a_name }}</p>
            </div>
            <div>
              <label class="block font-black mb-2 ml-4">反方立场</label>
              <input v-model="createForm.side_b_name" class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50" placeholder="比如：逻辑至上" type="text" />
              <p v-if="createErrors.side_b_name" class="mt-2 ml-4 text-sm font-black text-red-600">{{ createErrors.side_b_name }}</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block font-black mb-2 ml-4">选择赛制</label>
              <select v-model="createForm.format" class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50">
                <option value="快嘴乱斗">快嘴乱斗</option>
                <option value="深蹲逻辑">深蹲逻辑</option>
                <option value="复读机模式">复读机模式</option>
              </select>
            </div>
            <div>
              <label class="block font-black mb-2 ml-4">分类</label>
              <select v-model="createForm.category" class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50">
                <option v-for="c in categoriesForSelect" :key="c" :value="c">{{ c }}</option>
              </select>
              <p v-if="createErrors.category" class="mt-2 ml-4 text-sm font-black text-red-600">{{ createErrors.category }}</p>
            </div>
          </div>
          <div class="p-6 bg-yellow-100 border-4 border-black border-dashed rounded-3xl font-bold text-sm">
            ⚠️ 温馨提示：请勿在辩论中使用物理攻击。虽然我们鼓励碰撞，但那是脑细胞的碰撞，不是骨头的碰撞。
          </div>
          <div v-if="createErrorMsg" class="bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
            {{ createErrorMsg }}
          </div>
          <button class="w-full bg-purple-600 text-white py-6 rounded-3xl text-2xl font-black border-4 border-black shadow-[8px_8px_0px_black] bouncy-btn disabled:opacity-50" :disabled="creatingTopic" type="submit">
            🔥 开启混战！
          </button>
        </form>
      </div>
    </div>

    <div v-show="successOpen" class="fixed inset-0 z-[300] flex items-center justify-center p-6 bg-accent/90">
      <div class="bg-white border-8 border-black p-12 rounded-[100px] text-center modal-enter max-w-md">
        <Icon class="text-yellow-400 mb-6" icon="mdi:flash-circle" width="100"></Icon>
        <h2 class="text-5xl humor-font font-black mb-4">话题开启！</h2>
        <p class="text-xl font-bold mb-8">话题已经成功丢进池子里了，水花溅到了三公里外的图书馆！</p>
        <button class="bg-black text-white px-10 py-4 rounded-full font-black text-xl bouncy-btn" type="button" @click="successOpen = false">快去围观</button>
      </div>
    </div>

    <footer class="bg-black py-12 mt-20 text-white">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center text-sm font-bold gap-6">
        <p>© 2026 思辩乐园 (Debate Paradise). 别吵了，大家都是好朋友。</p>
        <div class="flex gap-10">
          <RouterLink class="hover:text-pink-500 transition-colors" to="/rules">游玩守则</RouterLink>
          <RouterLink class="hover:text-yellow-400 transition-colors" to="/resources">秘密中心</RouterLink>
          <RouterLink class="hover:text-mint transition-colors" to="/about">拍拍我们</RouterLink>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import FloatingNav from '../components/layout/FloatingNav.vue'
import MainNav from '../components/layout/MainNav.vue'
import { http } from '../api/http'
import { useAuthStore } from '../stores/auth'

const createModalOpen = ref(false)
const successOpen = ref(false)

const topics = ref([])
const topicsError = ref('')
const loadingTopics = ref(false)
const hasMore = ref(false)
const page = ref(1)
const pageSize = 30

const queryText = ref('')
const queryCategory = ref('')
const sortMode = ref('hot')
const searchDebounce = ref(null)

const categories = ref([])
const categoriesForSelect = ref(['综合'])

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const openCreate = () => {
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  resetCreateForm()
  createModalOpen.value = true
}

/** 与资料页「发起话题」一致：/debate-list?create=1 */
const tryOpenFromQuery = () => {
  const c = route.query.create
  if (c !== '1' && c !== 1) return
  if (!auth.isAuthed) {
    router.replace({ path: '/login', query: { redirect: '/debate-list?create=1' } })
    return
  }
  resetCreateForm()
  createModalOpen.value = true
  const q = { ...route.query }
  delete q.create
  router.replace({ path: '/debate-list', query: q })
}

const closeCreate = () => {
  createModalOpen.value = false
}

const createForm = ref({
  title: '',
  description: '',
  side_a_name: '',
  side_b_name: '',
  category: '综合',
  format: '快嘴乱斗'
})
const createErrors = ref({})
const creatingTopic = ref(false)
const createErrorMsg = ref('')

const resetCreateForm = () => {
  const preferredCategory = queryCategory.value || (categories.value[0]?.category || '') || '综合'
  createForm.value = {
    title: '',
    description: '',
    side_a_name: '',
    side_b_name: '',
    category: preferredCategory,
    format: '快嘴乱斗'
  }
  createErrors.value = {}
  createErrorMsg.value = ''
}

const submitCreate = async () => {
  if (creatingTopic.value) return
  creatingTopic.value = true
  createErrors.value = {}
  createErrorMsg.value = ''
  try {
    const payload = {
      title: createForm.value.title,
      description: createForm.value.description,
      category: createForm.value.category,
      format: createForm.value.format,
      side_a_name: createForm.value.side_a_name,
      side_b_name: createForm.value.side_b_name
    }
    const r = await http.post('topics/', payload)
    createModalOpen.value = false
    successOpen.value = true
    await loadTopics({ resetPage: true })
    const id = r?.item?.id
    if (id) {
      router.push({ path: '/debate-detail', query: { id: String(id) } })
    }
  } catch (e) {
    const data = e?.response?.data?.data
    if (data && typeof data === 'object') {
      const next = {}
      for (const [k, v] of Object.entries(data)) next[k] = Array.isArray(v) ? v[0] : String(v)
      createErrors.value = next
    }
    createErrorMsg.value = e?.message || '创建失败'
  } finally {
    creatingTopic.value = false
  }
}

const toK = (n) => {
  const v = Number(n || 0)
  if (v >= 10000) return `${(v / 10000).toFixed(1)}w`
  if (v >= 1000) return `${(v / 1000).toFixed(1)}k`
  return String(v)
}

const categoryPillBg = (idx) => {
  if (idx % 3 === 1) return 'bg-blue-300'
  if (idx % 3 === 2) return 'bg-yellow-300'
  return 'bg-yellow-300'
}

const loadCategories = async () => {
  try {
    const r = await http.get('topics/categories/')
    const items = Array.isArray(r?.items) ? r.items : []
    categories.value = items
      .map((x) => ({ category: String(x?.category || '').trim(), count: Number(x?.count || 0) }))
      .filter((x) => x.category)
      .slice(0, 12)
    if (!categories.value.some((x) => x.category === '综合')) {
      categories.value.push({ category: '综合', count: 0 })
    }
    const sorted = categories.value.map((x) => x.category)
    if (!sorted.includes('综合')) sorted.push('综合')
    categoriesForSelect.value = sorted
  } catch {
    categories.value = [
      { category: '哲学脑洞', count: 0 },
      { category: '科技拆解', count: 0 },
      { category: '社恐日常', count: 0 },
      { category: '综合', count: 0 }
    ]
    categoriesForSelect.value = categories.value.map((x) => x.category)
  }
}

const filterBtnClass = (value, hoverClass = 'hover:bg-yellow-300') => {
  const active = queryCategory.value === value
  return [
    'px-6',
    'py-2',
    'border-2',
    'border-black',
    'rounded-full',
    'font-black',
    'bouncy-btn',
    'shadow-[3px_3px_0px_black]',
    'whitespace-nowrap',
    'transition-all',
    active ? 'bg-pink-500 text-white' : `bg-white text-black ${hoverClass}`
  ].join(' ')
}

const sortBtnClass = (value) => {
  const active = sortMode.value === value
  return [
    'px-5',
    'py-2',
    'border-4',
    'border-black',
    'rounded-2xl',
    'font-black',
    'shadow-[4px_4px_0px_black]',
    'transition-all',
    active ? 'bg-black text-white' : 'bg-white text-black hover:bg-yellow-400'
  ].join(' ')
}

const setCategory = (v) => {
  queryCategory.value = v
  loadTopics({ resetPage: true })
}

const setSort = (v) => {
  sortMode.value = v
  loadTopics({ resetPage: true })
}

const goPage = (next) => {
  if (loadingTopics.value) return
  if (next < 1) return
  if (next > page.value && !hasMore.value) return
  page.value = next
  loadTopics()
}

const reload = () => loadTopics()

const loadTopics = async ({ resetPage } = {}) => {
  topicsError.value = ''
  loadingTopics.value = true
  if (resetPage) page.value = 1
  try {
    const r = await http.get('topics/', {
      params: {
        limit: pageSize,
        page: page.value,
        q: queryText.value.trim() || undefined,
        category: queryCategory.value || undefined,
        sort: sortMode.value || undefined
      }
    })
    topics.value = r?.items || []
    hasMore.value = Boolean(r?.has_more ?? r?.hasMore)
  } catch (e) {
    topicsError.value = e?.message || '加载失败'
    topics.value = []
    hasMore.value = false
  }
  loadingTopics.value = false
}

watch(
  () => queryText.value,
  () => {
    if (searchDebounce.value) clearTimeout(searchDebounce.value)
    searchDebounce.value = setTimeout(() => {
      loadTopics({ resetPage: true })
    }, 350)
  }
)

watch(
  () => [route.query.create, auth.isAuthed],
  () => tryOpenFromQuery()
)

onMounted(() => {
  loadCategories().finally(() => {
    loadTopics()
    tryOpenFromQuery()
  })
})
</script>

<style>
.neo-card {
  background: white;
  border: 4px solid black;
  box-shadow: 8px 8px 0px black;
  transition: all 0.2s;
}

.neo-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 12px 12px 0px black;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(-1deg);
}

.category-pill {
  border: 2px solid black;
  box-shadow: 3px 3px 0px black;
}

.abstract-dot {
  position: absolute;
  border-radius: 50%;
  z-index: -1;
  opacity: 0.3;
}

.modal-enter {
  animation: modalEnter 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes modalEnter {
  0% {
    transform: scale(0.7) rotate(10deg);
    opacity: 0;
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}
</style>
