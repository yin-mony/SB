<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <header class="bg-mint py-20 text-black text-center relative overflow-hidden border-b-4 border-black">
      <div class="absolute top-10 left-10 text-pink-500 opacity-40 rotate-12">
        <Icon class="float-slow" icon="mdi:thought-bubble" width="120"></Icon>
      </div>
      <div class="absolute bottom-10 right-10 text-accent opacity-40 -rotate-12">
        <Icon class="float-fast" icon="mdi:script-text-outline" width="120"></Icon>
      </div>
      <div class="max-w-7xl mx-auto px-6 relative z-10">
        <h1 class="text-6xl humor-font font-black mb-6">📝 胡说八道 (有理有据版)</h1>
        <p class="text-xl font-bold max-w-2xl mx-auto leading-relaxed mb-10">
          这些文章看起来像是在开玩笑，但细读之下你会发现...<br />
          嗯，它们确实是在开玩笑，只是很有逻辑。
        </p>
        <button
          class="bg-black text-yellow-400 text-3xl font-black px-12 py-6 rounded-3xl bouncy-btn border-4 border-black shadow-[10px_10px_0px_#ff477e] hover:rotate-2"
          type="button"
          @click="openCreateModal"
        >
          📢 发起胡说！
        </button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-20">
      <div class="flex flex-wrap gap-4 mb-16 justify-center">
        <button
          type="button"
          :class="filterBtnClass(listFilter === 'all')"
          @click="setListFilter('all')"
        >
          📚 全部最新
        </button>
        <button
          type="button"
          :class="filterBtnClass(listFilter === 'hot')"
          @click="setListFilter('hot')"
        >
          🔥 热门八道
        </button>
        <button
          type="button"
          :class="filterBtnClass(listFilter === '逻辑体操')"
          @click="setListFilter('逻辑体操')"
        >
          🥗 营养鸡汤
        </button>
        <button
          type="button"
          :class="filterBtnClass(listFilter === '职场歪理')"
          @click="setListFilter('职场歪理')"
        >
          👻 灵异逻辑
        </button>
        <button
          type="button"
          :class="filterBtnClass(listFilter === '赛博生活')"
          @click="setListFilter('赛博生活')"
        >
          👾 赛博黑洞
        </button>
      </div>

      <div v-if="listLoading" class="text-center py-20 font-black text-slate-500">加载中…</div>
      <div v-else-if="listError" class="neo-card p-8 rounded-[40px] text-center max-w-xl mx-auto mb-12">
        <p class="font-black text-red-600 mb-4">{{ listError }}</p>
        <button type="button" class="bouncy-btn px-8 py-3 bg-black text-white rounded-full font-black" @click="reloadList">
          重试
        </button>
      </div>
      <div v-else-if="!posts.length" class="text-center py-20 font-black text-slate-500">这里还空空如也，来做第一条胡说？</div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-16">
        <RouterLink
          v-for="(p, idx) in posts"
          :key="p.id"
          v-reveal="idx * 60"
          :class="['blob-card p-8 flex flex-col group cursor-pointer', idx % 3 === 1 ? 'bg-pink-100/50' : '']"
          :to="{ path: '/blog-detail', query: { id: String(p.id), slug: p.slug } }"
        >
          <div
            :class="[
              'relative mb-8 h-60 overflow-hidden border-4 border-black transition-transform',
              idx % 3 === 0 ? 'rounded-[40px] group-hover:rotate-[-2deg]' : idx % 3 === 1 ? 'rounded-[20px_60px_20px_60px] group-hover:rotate-[2deg]' : 'rounded-[50%_50%_10%_10%] group-hover:scale-95'
            ]"
          >
            <img alt="blog" class="w-full h-full object-cover" :src="p.cover_image || fallbackCover(p.id)" />
            <div v-if="idx === 0 && listFilter === 'hot'" class="absolute top-4 left-4 bg-yellow-400 border-2 border-black px-4 py-1 rounded-full font-black text-xs">
              ⭐ 必读脑洞
            </div>
            <div v-else-if="idx === 0" class="absolute top-4 left-4 bg-yellow-400 border-2 border-black px-4 py-1 rounded-full font-black text-xs">⭐ 新鲜出炉</div>
          </div>
          <div class="flex-1">
            <p class="text-pink-600 font-black mb-2 uppercase tracking-tighter"># {{ p.category }}</p>
            <h3 class="text-3xl font-black mb-4 leading-snug group-hover:text-accent transition-colors">{{ p.title }}</h3>
            <p class="text-slate-600 font-bold mb-6 line-clamp-3">
              {{ p.excerpt || '（作者正在憋大招…）' }}
            </p>
          </div>
          <div class="pt-6 border-t-4 border-black flex items-center justify-between">
            <div class="flex items-center gap-3">
              <img
                alt="author"
                class="w-10 h-10 rounded-full border-2 border-black"
                :src="p.author?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(p.author?.username || 'author')}`"
              />
              <span class="font-black text-sm">{{ p.author?.username || '匿名作者' }}</span>
            </div>
            <span class="text-xs font-black bg-slate-200 px-2 py-1 border border-black">阅读 {{ toK(p.view_count || 0) }}</span>
          </div>
        </RouterLink>
      </div>

      <div v-if="posts.length && listHasMore" class="flex justify-center mt-12">
        <button
          type="button"
          class="px-10 py-4 border-4 border-black rounded-full font-black bg-white bouncy-btn shadow-[6px_6px_0px_black] disabled:opacity-50"
          :disabled="listLoadingMore"
          @click="loadMorePosts"
        >
          {{ listLoadingMore ? '加载中…' : '加载更多胡说' }}
        </button>
      </div>

      <section class="mt-32 bg-yellow-400 border-8 border-black p-12 rounded-[60px] shadow-[15px_15px_0px_black] text-center max-w-4xl mx-auto">
        <h2 class="text-5xl humor-font font-black mb-6">📭 别错过我的瞎话</h2>
        <p class="text-xl font-bold mb-10 text-black/80">
          订阅我们的每周“胡说周报”，我们保证不会发任何有用的学术内容。<br />
          只有最纯正的、能让你在聚会上显得很有逻辑的废话。
        </p>
        <div class="flex flex-col md:flex-row gap-4 max-w-2xl mx-auto">
          <input
            v-model="nlEmail"
            class="flex-1 px-8 py-5 border-4 border-black rounded-3xl text-xl font-bold bg-white focus:outline-none"
            placeholder="把你的邮箱丢进来..."
            type="email"
            autocomplete="email"
            :disabled="nlSubmitting"
          />
          <button
            type="button"
            class="bg-pink-500 text-white px-10 py-5 border-4 border-black rounded-3xl text-xl font-black bouncy-btn shadow-[6px_6px_0px_black] disabled:opacity-50"
            :disabled="nlSubmitting"
            @click="submitNewsletter"
          >
            {{ nlSubmitting ? '投喂中…' : '立即投喂' }}
          </button>
        </div>
        <p v-if="nlMessage" class="mt-6 font-black text-black">{{ nlMessage }}</p>
        <p v-if="nlError" class="mt-4 font-black text-red-800">{{ nlError }}</p>
      </section>
    </main>

    <div v-show="createModalOpen" class="fixed inset-0 z-[200] flex items-center justify-center p-6 bg-black/80 backdrop-blur-sm">
      <div class="bg-white border-8 border-black w-full max-w-2xl rounded-[60px] p-10 modal-enter overflow-y-auto max-h-[90vh]">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-4xl humor-font font-black">{{ editingPostId ? '✏️ 修改你的神逻辑' : '📝 提交你的神逻辑' }}</h2>
          <button
            class="w-12 h-12 border-4 border-black rounded-full flex items-center justify-center hover:bg-red-500 hover:text-white transition-colors"
            type="button"
            @click="closeCreateModal"
          >
            <Icon icon="mdi:close" width="30"></Icon>
          </button>
        </div>
        <p v-if="createError" class="mb-4 p-4 bg-red-100 border-4 border-black rounded-2xl font-black text-red-700">{{ createError }}</p>
        <form class="space-y-6" @submit.prevent="submitBlog">
          <div>
            <label class="block font-black mb-2 ml-4 text-xl">文章标题 (语不惊人死不休)</label>
            <input
              v-model="formTitle"
              class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50 focus:outline-none"
              placeholder="比如：如何优雅地在水下吃火锅？"
              required
              type="text"
              maxlength="200"
              :disabled="createSubmitting"
            />
          </div>
          <div>
            <label class="block font-black mb-2 ml-4 text-xl">内容 (支持富文本/Markdown)</label>
            <textarea
              v-model="formContent"
              class="w-full p-6 border-4 border-black rounded-3xl font-bold bg-slate-50 focus:outline-none h-48"
              placeholder="在这里倾倒你的知识垃圾... (此处应有富文本编辑器)"
              required
              :disabled="createSubmitting"
            ></textarea>
          </div>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block font-black mb-2 ml-4">分类</label>
              <select v-model="formCategory" class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50" :disabled="createSubmitting">
                <option value="逻辑体操">逻辑体操</option>
                <option value="赛博生活">赛博生活</option>
                <option value="职场歪理">职场歪理</option>
              </select>
            </div>
            <div>
              <label class="block font-black mb-2 ml-4">标签</label>
              <input
                v-model="formTags"
                class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50"
                placeholder="多标签用逗号分隔"
                type="text"
                :disabled="createSubmitting"
              />
            </div>
          </div>
          <div>
            <label class="block font-black mb-2 ml-4">封面图上传 (或者丢个链接)</label>
            <input ref="coverFileInput" class="hidden" type="file" accept="image/png,image/jpeg,image/jpg,image/webp,image/gif" @change="onCoverFile" />
            <input
              v-model="formCoverUrl"
              class="w-full p-4 border-4 border-black rounded-3xl font-bold bg-slate-50 mb-4"
              placeholder="https://... 或先上传图片"
              type="url"
              :disabled="createSubmitting"
            />
            <button
              type="button"
              class="w-full border-4 border-dashed border-black p-8 rounded-3xl text-center bg-slate-100 hover:bg-slate-200 disabled:opacity-50"
              :disabled="createSubmitting || coverUploading"
              @click="coverFileInput?.click()"
            >
              <Icon class="text-slate-400" icon="mdi:cloud-upload" width="48"></Icon>
              <p class="font-black mt-2">{{ coverUploading ? '上传中…' : '把图片甩到这里！' }}</p>
            </button>
          </div>
          <button
            class="w-full bg-mint py-6 rounded-3xl text-2xl font-black border-4 border-black shadow-[8px_8px_0px_black] bouncy-btn disabled:opacity-50"
            type="submit"
            :disabled="createSubmitting"
          >
            {{ createSubmitting ? '保存中…' : editingPostId ? '💾 保存修改' : '🚀 确认发射！' }}
          </button>
        </form>
      </div>
    </div>

    <div v-show="successOpen" class="fixed inset-0 z-[300] flex items-center justify-center p-6 bg-pink-500/90">
      <div class="bg-white border-8 border-black p-12 rounded-[100px] text-center modal-enter max-w-md">
        <Icon class="text-yellow-400 mb-6" icon="mdi:party-popper" width="100"></Icon>
        <h2 class="text-5xl humor-font font-black mb-4">{{ lastSaveWasEdit ? '保存成功！' : '发射成功！' }}</h2>
        <p class="text-xl font-bold mb-8">
          {{
            lastSaveWasEdit
              ? '改动已生效，宇宙中的兔子翻了个身表示已阅。'
              : '你的神逻辑已经在宇宙中回荡了，甚至惊动了正在月球午睡的兔子！'
          }}
        </p>
        <div class="flex flex-col gap-3">
          <button
            v-if="createdPostId"
            class="bg-black text-white px-10 py-4 rounded-full font-black text-xl bouncy-btn"
            type="button"
            @click="goCreatedPost"
          >
            去看我的文章
          </button>
          <button class="bg-slate-200 text-black px-10 py-4 rounded-full font-black text-xl bouncy-btn" type="button" @click="successOpen = false">
            太棒了，滚回去继续看
          </button>
        </div>
      </div>
    </div>

    <footer class="bg-black py-12 text-white">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <p class="font-black text-xl humor-font mb-4">思辩乐园 - 让知识变好玩</p>
        <p class="text-slate-400 font-bold">© 2026 我们不生产真理，我们只是真理的搬运工（顺便把它拆了）。</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import FloatingNav from '../components/layout/FloatingNav.vue'
import MainNav from '../components/layout/MainNav.vue'
import { http } from '../api/http'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const createModalOpen = ref(false)
const successOpen = ref(false)
const posts = ref([])
const listFilter = ref('all')
const listOffset = ref(0)
const listHasMore = ref(false)
const listLoading = ref(true)
const listLoadingMore = ref(false)
const listError = ref('')

const nlEmail = ref('')
const nlSubmitting = ref(false)
const nlMessage = ref('')
const nlError = ref('')

const formTitle = ref('')
const formContent = ref('')
const formCategory = ref('逻辑体操')
const formTags = ref('')
const formCoverUrl = ref('')
const coverFileInput = ref(null)
const coverUploading = ref(false)
const createSubmitting = ref(false)
const createError = ref('')
const createdPostId = ref(null)
const createdSlug = ref('')
const editingPostId = ref(null)
const lastSaveWasEdit = ref(false)

const filterBtnClass = (active) =>
  active
    ? 'px-8 py-3 bg-black text-yellow-300 rounded-full font-black text-lg bouncy-btn border-4 border-black shadow-[4px_4px_0px_#ff477e]'
    : 'px-8 py-3 bg-white border-4 border-black rounded-full font-black text-lg bouncy-btn hover:bg-yellow-400'

const listParams = () => {
  const params = { limit: 12, offset: listOffset.value }
  if (listFilter.value === 'hot') params.sort = 'hot'
  else if (listFilter.value !== 'all') params.category = listFilter.value
  return params
}

const applyPostsResponse = (data, append) => {
  const chunk = data?.items || []
  if (append) posts.value = [...posts.value, ...chunk]
  else posts.value = chunk
  listHasMore.value = !!data?.has_more
  if (data?.has_more && data?.next_offset != null) {
    listOffset.value = data.next_offset
  } else if (!append && !data?.has_more) {
    listOffset.value = 0
  }
}

const loadPosts = async (append) => {
  if (append) {
    listLoadingMore.value = true
  } else {
    listLoading.value = true
    listError.value = ''
  }
  try {
    const r = await http.get('blog-posts/', { params: listParams() })
    applyPostsResponse(r, append)
  } catch (e) {
    if (!append) {
      listError.value = e?.message || '加载失败'
      posts.value = []
      listHasMore.value = false
    }
  } finally {
    listLoading.value = false
    listLoadingMore.value = false
  }
}

const reloadList = () => {
  listOffset.value = 0
  loadPosts(false)
}

const setListFilter = (key) => {
  listFilter.value = key
}

watch(listFilter, () => {
  listOffset.value = 0
  loadPosts(false)
})

const loadMorePosts = async () => {
  if (!listHasMore.value || listLoadingMore.value) return
  await loadPosts(true)
}

const resetCreateForm = () => {
  formTitle.value = ''
  formContent.value = ''
  formTags.value = ''
  formCoverUrl.value = ''
  formCategory.value = '逻辑体操'
}

const closeCreateModal = () => {
  createModalOpen.value = false
  editingPostId.value = null
}

const openCreateModal = () => {
  createError.value = ''
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: '/blog' } })
    return
  }
  editingPostId.value = null
  resetCreateForm()
  createModalOpen.value = true
}

const loadPostForEdit = async (id) => {
  createError.value = ''
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: `/blog?edit=${id}` } })
    return false
  }
  try {
    const r = await http.get(`blog-posts/${id}/`)
    const item = r?.item
    if (!item) {
      createError.value = '找不到文章或无权编辑'
      return false
    }
    formTitle.value = item.title || ''
    formContent.value = item.content || ''
    formCategory.value = item.category || '逻辑体操'
    const tags = item.tags
    formTags.value = Array.isArray(tags) ? tags.join(',') : typeof tags === 'string' ? tags : ''
    formCoverUrl.value = item.cover_image || ''
    editingPostId.value = id
    createModalOpen.value = true
    router.replace({ path: '/blog' })
    return true
  } catch (e) {
    createError.value = e?.message || '加载失败'
    return false
  }
}

const tryOpenFromRoute = () => {
  const e = route.query.edit
  const c = route.query.create
  const raw = Array.isArray(e) ? e[0] : e
  const id = Number(raw)
  if (raw !== undefined && raw !== null && raw !== '' && Number.isFinite(id) && id > 0) {
    loadPostForEdit(id)
  } else if (c === '1' || c === 1) {
    if (!auth.isAuthed) {
      router.push({ path: '/login', query: { redirect: '/blog?create=1' } })
      return
    }
    editingPostId.value = null
    resetCreateForm()
    createModalOpen.value = true
    router.replace({ path: '/blog' })
  }
}

const onCoverFile = async (ev) => {
  const file = ev.target?.files?.[0]
  if (!file) return
  createError.value = ''
  coverUploading.value = true
  try {
    const fd = new FormData()
    fd.append('file', file)
    const r = await http.post('blog-posts/covers/upload/', fd)
    if (r?.cover_image) formCoverUrl.value = r.cover_image
  } catch (e) {
    createError.value = e?.message || '封面上传失败'
  } finally {
    coverUploading.value = false
    ev.target.value = ''
  }
}

const submitBlog = async () => {
  createError.value = ''
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: '/blog' } })
    return
  }
  createSubmitting.value = true
  const editId = editingPostId.value
  try {
    const tags = formTags.value
      .split(/[,，]/)
      .map((s) => s.trim())
      .filter(Boolean)
    const payload = {
      title: formTitle.value.trim(),
      content: formContent.value.trim(),
      category: formCategory.value,
      tags,
      cover_image: formCoverUrl.value.trim() || undefined
    }
    if (editingPostId.value) {
      const r = await http.patch(`blog-posts/${editingPostId.value}/`, payload)
      const item = r?.item
      createdPostId.value = item?.id || editingPostId.value
      createdSlug.value = item?.slug || ''
      lastSaveWasEdit.value = true
      resetCreateForm()
      closeCreateModal()
      successOpen.value = true
    } else {
      const r = await http.post('blog-posts/', payload)
      const item = r?.item
      createdPostId.value = item?.id || null
      createdSlug.value = item?.slug || ''
      lastSaveWasEdit.value = false
      closeCreateModal()
      successOpen.value = true
      resetCreateForm()
    }
    listOffset.value = 0
    await loadPosts(false)
  } catch (e) {
    createError.value = e?.message || (editId ? '保存失败' : '发布失败')
  } finally {
    createSubmitting.value = false
  }
}

const goCreatedPost = () => {
  successOpen.value = false
  if (createdPostId.value) {
    router.push({ path: '/blog-detail', query: { id: String(createdPostId.value), slug: createdSlug.value || undefined } })
  }
}

const submitNewsletter = async () => {
  nlMessage.value = ''
  nlError.value = ''
  nlSubmitting.value = true
  try {
    const r = await http.post('blog-posts/subscribe-newsletter/', { email: nlEmail.value.trim() })
    if (r?.already) nlMessage.value = '你早就订阅过了，但我们还是开心地又记了一笔。'
    else nlMessage.value = '订阅成功！周报会在某个随机的周二（也可能不是周二）抵达。'
    nlEmail.value = ''
  } catch (e) {
    nlError.value = e?.message || '订阅失败'
  } finally {
    nlSubmitting.value = false
  }
}

const toK = (n) => {
  const v = Number(n || 0)
  if (v >= 10000) return `${(v / 10000).toFixed(1)}w`
  if (v >= 1000) return `${(v / 1000).toFixed(1)}k`
  return String(v)
}

const fallbackCover = (seed) => {
  const s = encodeURIComponent(String(seed || 'cover'))
  return `https://images.unsplash.com/photo-1518020382113-a7e8fc38eac9?w=600&auto=format&fit=crop&sig=${s}`
}

watch(
  () => [route.query.edit, route.query.create, auth.isAuthed],
  () => {
    tryOpenFromRoute()
  }
)

onMounted(() => {
  loadPosts(false)
  const e = route.query.edit
  if ((e !== undefined && e !== null && e !== '') && !auth.isAuthed) {
    const raw = Array.isArray(e) ? e[0] : e
    router.replace({ path: '/login', query: { redirect: `/blog?edit=${encodeURIComponent(String(raw))}` } })
    return
  }
  tryOpenFromRoute()
})
</script>

<style>
.blob-card {
  background: white;
  border: 4px solid black;
  box-shadow: 10px 10px 0px black;
  transition: all 0.3s;
  border-radius: 60px 20px 60px 20px;
}

.blob-card:hover {
  transform: scale(1.02) rotate(1deg);
  box-shadow: 15px 15px 0px black;
  border-radius: 20px 60px 20px 60px;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.1) rotate(-2deg);
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
