<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <main class="max-w-4xl mx-auto px-6 py-12">
      <article class="neo-card p-10 rounded-[40px] relative overflow-hidden mb-12">
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-pink-500/10 rounded-full blur-3xl"></div>
        <header class="mb-10">
          <div class="flex items-center gap-4 mb-6">
            <span class="px-4 py-1 bg-black text-white rounded-full font-black text-sm"># {{ post?.category || '分类' }}</span>
            <span class="text-slate-500 font-bold">{{ dateText }}</span>
          </div>
          <h1 class="text-5xl md:text-6xl humor-font font-black mb-8 leading-tight">{{ post?.title || '文章加载中...' }}</h1>
          <div class="flex items-center justify-between p-6 bg-slate-100 rounded-3xl border-2 border-black border-dashed">
            <div class="flex items-center gap-4">
              <img
                alt="author"
                class="w-16 h-16 rounded-full border-4 border-black"
                :src="post?.author?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(post?.author?.username || 'author')}`"
              />
              <div>
                <p class="font-black text-xl">{{ post?.author?.username || '匿名作者' }}</p>
                <p class="text-sm font-bold text-slate-500">{{ post?.author?.bio || '该作者暂无简介' }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button class="bg-white text-black px-6 py-2 rounded-xl font-black bouncy-btn border-2 border-black" type="button" @click="toggleFavorite">
                {{ isFavorited ? '💔 取消收藏' : '🔖 收藏' }}
              </button>
              <button
                v-if="showFollowBtn"
                class="bg-black text-white px-6 py-2 rounded-xl font-black bouncy-btn"
                type="button"
                @click="toggleFollow"
              >
                {{ isFollowing ? '已关注' : '+ 关注' }}
              </button>
            </div>
          </div>
        </header>
        <div class="rich-content text-slate-800" v-html="contentHtml"></div>
        <div class="mt-16 flex flex-wrap gap-4">
          <span v-for="(t, idx) in (post?.tags || [])" :key="`${t}-${idx}`" class="px-6 py-2 border-4 border-black rounded-full font-black" :class="tagClass(idx)">
            # {{ t }}
          </span>
        </div>
        <p v-if="postActionError" class="mt-6 font-black text-red-600">{{ postActionError }}</p>
        <div v-if="isAuthor && post" class="mt-8 flex flex-wrap gap-3 justify-end items-center">
          <span v-if="post.is_published === false" class="font-black text-red-600 mr-auto text-sm">已下架，仅你可见。</span>
          <RouterLink
            v-if="post.is_published !== false"
            class="bg-yellow-400 text-black px-5 py-2 rounded-xl font-black border-4 border-black bouncy-btn text-sm"
            :to="{ path: '/blog', query: { edit: String(post.id) } }"
          >
            ✏️ 编辑
          </RouterLink>
          <button
            v-if="post.is_published !== false"
            class="bg-white text-red-700 px-5 py-2 rounded-xl font-black border-4 border-red-600 bouncy-btn text-sm"
            type="button"
            @click="withdrawPost"
          >
            撤回上架
          </button>
          <button
            v-if="post.is_published === false"
            class="bg-mint text-black px-5 py-2 rounded-xl font-black border-4 border-black bouncy-btn text-sm"
            type="button"
            @click="republishPost"
          >
            重新上架
          </button>
        </div>
      </article>

      <section class="neo-card p-10 rounded-[40px] mb-12">
        <h3 class="text-3xl humor-font font-black mb-8 flex items-center gap-3">
          <Icon class="text-pink-500" icon="mdi:comment-text-multiple"></Icon>
          看看他们在胡说什么 ({{ commentsCount }})
        </h3>
        <div class="space-y-8">
          <div class="flex gap-4">
            <img
              alt="me"
              class="w-12 h-12 rounded-full border-2 border-black"
              :src="commenterAvatar"
            />
            <div class="flex-1 relative">
              <textarea
                v-model="commentText"
                class="w-full p-6 border-4 border-black rounded-3xl font-bold bg-slate-50 focus:outline-none min-h-[120px]"
                placeholder="输入你的神逻辑..."
                @keyup.enter.exact.prevent="submitComment()"
              ></textarea>
              <div class="absolute bottom-4 right-4 flex items-center gap-3">
                <button
                  v-if="autoMode"
                  class="bg-black text-white px-5 py-2 rounded-xl border-2 border-black font-black bouncy-btn disabled:opacity-50"
                  :disabled="commenting"
                  type="button"
                  @click="autoSendComment"
                >
                  🤖 一键抬杠
                </button>
                <button
                  class="bg-pink-500 text-white px-6 py-2 rounded-xl border-2 border-black font-black bouncy-btn disabled:opacity-50"
                  :disabled="commenting || !commentText.trim()"
                  type="button"
                  @click="submitComment()"
                >
                  发射！
                </button>
              </div>
            </div>
          </div>
          <div v-if="commentError" class="bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
            {{ commentError }}
          </div>

          <div v-for="c in topLevelComments" :key="c.id" class="space-y-3">
            <div class="flex gap-4">
              <img
                alt="reader"
                class="w-12 h-12 rounded-full border-2 border-black"
                :src="c.user?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(c.user?.username || 'reader')}`"
              />
              <div class="flex-1">
                <div class="bg-white border-4 border-black p-6 rounded-3xl rounded-tl-none">
                  <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                    <p class="font-black text-accent">
                      {{ c.user?.username || '匿名' }} <span class="text-xs text-slate-400 ml-2">{{ formatDateTime(c.created_at) }}</span>
                    </p>
                    <button
                      v-if="canShowDeleteForComment(c)"
                      class="text-xs font-black text-red-600 underline disabled:opacity-50"
                      type="button"
                      :disabled="commentDeletingId === c.id"
                      @click="deleteComment(c)"
                    >
                      {{ commentDeletingId === c.id ? '删除中…' : '删除' }}
                    </button>
                  </div>
                  <p class="font-bold">{{ c.content }}</p>
                </div>
              </div>
            </div>
            <div v-if="repliesByParent[c.id]?.length" class="ml-16 space-y-3">
              <div v-for="r in repliesByParent[c.id]" :key="r.id" class="flex gap-4">
                <img
                  alt="reader"
                  class="w-10 h-10 rounded-full border-2 border-black"
                  :src="r.user?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(r.user?.username || 'reader')}`"
                />
                <div class="flex-1">
                  <div class="bg-slate-50 border-4 border-black p-5 rounded-3xl rounded-tl-none">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                      <p class="font-black text-accent">
                        {{ r.user?.username || '匿名' }} <span class="text-xs text-slate-400 ml-2">{{ formatDateTime(r.created_at) }}</span>
                      </p>
                      <button
                        v-if="canShowDeleteForComment(r)"
                        class="text-xs font-black text-red-600 underline disabled:opacity-50"
                        type="button"
                        :disabled="commentDeletingId === r.id"
                        @click="deleteComment(r)"
                      >
                        {{ commentDeletingId === r.id ? '删除中…' : '删除' }}
                      </button>
                    </div>
                    <p class="font-bold">{{ r.content }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button
          v-if="commentsHasMore"
          type="button"
          class="w-full mt-10 py-4 border-4 border-black border-dashed rounded-3xl font-black text-slate-600 hover:text-black transition-colors disabled:opacity-50"
          :disabled="commentsLoadingMore"
          @click="loadMoreComments"
        >
          {{ commentsLoadingMore ? '加载中…' : '加载更多废话...' }}
        </button>
      </section>

      <section v-if="relatedPosts.length" class="mb-20">
        <h3 class="text-3xl humor-font font-black mb-8">延伸阅读 (更多歪理)</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <RouterLink
            v-for="(rp, ridx) in relatedPosts.slice(0, 4)"
            :key="rp.id"
            class="neo-card p-6 rounded-3xl transition-colors flex gap-4"
            :class="ridx % 2 === 0 ? 'hover:bg-yellow-100' : 'hover:bg-pink-100'"
            :to="{ path: '/blog-detail', query: { id: String(rp.id), slug: rp.slug } }"
          >
            <img
              alt="thumb"
              class="w-24 h-24 rounded-2xl border-2 border-black object-cover shrink-0"
              :src="rp.cover_image || fallbackThumb(rp.id)"
            />
            <div class="min-w-0">
              <h4 class="font-black text-lg mb-2 leading-snug">{{ rp.title }}</h4>
              <p class="text-xs font-bold text-slate-500 line-clamp-2">{{ rp.excerpt || '（暂无摘要）' }}</p>
            </div>
          </RouterLink>
        </div>
      </section>
    </main>

    <footer class="bg-black py-12 text-white mt-20">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <p class="font-black text-xl humor-font mb-4">思辩乐园 - 让知识变好玩</p>
        <p class="text-slate-400 font-bold">© 2026 我们不生产真理，我们只是真理的搬运工（顺便把它拆了）。</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import hljs from 'highlight.js'
import { marked } from 'marked'
import FloatingNav from '../components/layout/FloatingNav.vue'
import MainNav from '../components/layout/MainNav.vue'
import { http } from '../api/http'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const post = ref(null)
const comments = ref([])
const relatedPosts = ref([])
const commentsHasMore = ref(false)
const commentsOffset = ref(0)
const commentsLoadingMore = ref(false)
const isFavorited = ref(false)
const isFollowing = ref(false)
const autoMode = computed(() => !!auth.user?.auto_debate_mode)

const commentText = ref('')
const commenting = ref(false)
const commentError = ref('')
const commentDeletingId = ref(0)

const postId = computed(() => {
  const v = route.query.id
  const id = Number(v || 0)
  return Number.isFinite(id) ? id : 0
})

const dateText = computed(() => {
  const v = post.value?.created_at
  if (!v) return ''
  const d = new Date(v)
  if (Number.isNaN(d.getTime())) return String(v)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}年${m}月${day}日`
})

const formatDateTime = (v) => {
  if (!v) return ''
  const d = new Date(v)
  if (Number.isNaN(d.getTime())) return String(v)
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  return `${y}-${m}-${day} ${hh}:${mm}`
}

const renderer = new marked.Renderer()
renderer.code = (code, infostring) => {
  const lang = (infostring || '').trim().split(/\s+/)[0]
  let value = ''
  if (lang && hljs.getLanguage(lang)) {
    value = hljs.highlight(String(code), { language: lang }).value
  } else {
    value = hljs.highlightAuto(String(code)).value
  }
  const cls = lang ? `hljs language-${lang}` : 'hljs'
  return `<pre><code class="${cls}">${value}</code></pre>`
}
marked.setOptions({ renderer, breaks: true })

const contentHtml = computed(() => {
  const md = post.value?.content || ''
  return marked.parse(md)
})

const repliesByParent = computed(() => {
  const map = {}
  for (const c of comments.value) {
    if (!c.parent_id) continue
    map[c.parent_id] = map[c.parent_id] || []
    map[c.parent_id].push(c)
  }
  return map
})

const topLevelComments = computed(() => comments.value.filter((c) => !c.parent_id))
const commentsCount = computed(() => comments.value.length)

const showFollowBtn = computed(() => {
  const authorId = post.value?.author?.id
  if (!authorId) return false
  if (!auth.isAuthed) return true
  if (auth.user?.id && auth.user.id === authorId) return false
  return true
})

const postActionError = ref('')
const isAuthor = computed(
  () => !!(auth.user?.id && post.value?.author?.id && auth.user.id === post.value.author.id)
)

const withdrawPost = async () => {
  if (!window.confirm('确定撤回？文章将从广场列表消失，你仍可编辑或重新上架。')) return
  postActionError.value = ''
  try {
    await http.delete(`blog-posts/${postId.value}/`)
    await loadPost()
  } catch (e) {
    postActionError.value = e?.message || '操作失败'
  }
}

const republishPost = async () => {
  postActionError.value = ''
  try {
    await http.patch(`blog-posts/${postId.value}/`, { is_published: true })
    await loadPost()
  } catch (e) {
    postActionError.value = e?.message || '操作失败'
  }
}

const commenterAvatar = computed(() => {
  const u = auth.user
  if (u?.avatar_url) return u.avatar_url
  const seed = encodeURIComponent(u?.username || 'guest')
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}`
})

const fallbackThumb = (id) =>
  `https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=200&auto=format&fit=crop&sig=${encodeURIComponent(String(id))}`

const tagClass = (idx) => {
  if (idx % 3 === 1) return 'bg-pink-400'
  if (idx % 3 === 2) return 'bg-accent text-white'
  return 'bg-yellow-400'
}

const loadPost = async () => {
  post.value = null
  comments.value = []
  relatedPosts.value = []
  commentsHasMore.value = false
  commentsOffset.value = 0
  if (!postId.value) return
  try {
    const [p, c, rel] = await Promise.all([
      http.get(`blog-posts/${postId.value}/`),
      http.get(`blog-posts/${postId.value}/comments/`, { params: { limit: 30, offset: 0 } }),
      http.get(`blog-posts/${postId.value}/related/`)
    ])
    post.value = p?.item || null
    comments.value = c?.items || []
    commentsHasMore.value = !!c?.has_more
    commentsOffset.value = c?.has_more ? c?.next_offset ?? (c?.items?.length || 0) : 0
    relatedPosts.value = rel?.items || []
  } catch {
    post.value = null
    comments.value = []
    relatedPosts.value = []
  }
}

const loadMoreComments = async () => {
  if (!postId.value || !commentsHasMore.value || commentsLoadingMore.value) return
  commentsLoadingMore.value = true
  try {
    const c = await http.get(`blog-posts/${postId.value}/comments/`, {
      params: { limit: 30, offset: commentsOffset.value }
    })
    const more = c?.items || []
    comments.value = [...comments.value, ...more]
    commentsHasMore.value = !!c?.has_more
    commentsOffset.value = c?.has_more ? c?.next_offset ?? commentsOffset.value + more.length : commentsOffset.value
  } finally {
    commentsLoadingMore.value = false
  }
}

const genAutoComment = () => {
  const title = post.value?.title || '这篇文章'
  const pool = [
    `关于「${title}」我有个不成熟的小建议：别成熟，继续胡说。`,
    `这篇写得太有道理了，我不允许它这么有道理。`,
    `你说得对，但我更想抬个杠：你还能更离谱一点吗？`,
    `我读完了，只想说一句：逻辑很顺，但情绪更顺。`,
    `建议作者把这篇刻在我的 CPU 上，方便我随时抬杠引用。`
  ]
  return pool[Math.floor(Math.random() * pool.length)]
}

const submitComment = async (contentOverride) => {
  commentError.value = ''
  const content = String(contentOverride ?? commentText.value ?? '').trim()
  if (!content) {
    commentError.value = '先写点东西再发射'
    return
  }
  if (!postId.value) return
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  commenting.value = true
  try {
    await http.post(`blog-posts/${postId.value}/comments/`, { content })
    commentText.value = ''
    await loadPost()
  } catch (e) {
    commentError.value = e?.message || '发送失败'
  } finally {
    commenting.value = false
  }
}

const autoSendComment = async () => {
  const content = genAutoComment()
  commentText.value = content
  await submitComment(content)
}

const canShowDeleteForComment = (c) => {
  if (!auth.isAuthed || !c) return false
  if (post.value?.author?.id === auth.user?.id) return true
  return c.user?.id === auth.user?.id
}

const deleteComment = async (c) => {
  if (!c?.id || !postId.value) return
  if (!window.confirm('确定删除这条评论？')) return
  commentDeletingId.value = c.id
  try {
    await http.delete(`blog-posts/${postId.value}/comments/${c.id}/`)
    await loadPost()
  } catch (e) {
    commentError.value = e?.message || '删除失败'
  } finally {
    commentDeletingId.value = 0
  }
}

const loadFavoriteStatus = async () => {
  isFavorited.value = false
  if (!auth.isAuthed || !postId.value) return
  try {
    const r = await http.get('favorites/status/', { params: { target_type: 'blog_post', target_id: postId.value } })
    isFavorited.value = !!r?.is_favorited
  } catch {
    isFavorited.value = false
  }
}

const toggleFavorite = async () => {
  if (!postId.value) return
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  if (isFavorited.value) {
    await http.delete('favorites/', { params: { target_type: 'blog_post', target_id: postId.value } })
  } else {
    await http.post('favorites/', { target_type: 'blog_post', target_id: postId.value })
  }
  await loadFavoriteStatus()
}

const loadFollowingStatus = async () => {
  isFollowing.value = false
  const authorId = post.value?.author?.id
  if (!auth.isAuthed || !auth.user?.id || !authorId) return
  if (auth.user.id === authorId) return
  try {
    const r = await http.get(`users/${auth.user.id}/following/`)
    const ids = new Set((r?.items || []).map((u) => u.id))
    isFollowing.value = ids.has(authorId)
  } catch {
    isFollowing.value = false
  }
}

const toggleFollow = async () => {
  const authorId = post.value?.author?.id
  if (!authorId) return
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  if (isFollowing.value) {
    await http.delete(`users/${authorId}/follow/`)
  } else {
    await http.post(`users/${authorId}/follow/`, {})
  }
  await loadFollowingStatus()
}

watch(
  () => postId.value,
  async () => {
    await loadPost()
    await loadFavoriteStatus()
    await loadFollowingStatus()
  },
  { immediate: true }
)

watch(
  () => auth.isAuthed,
  () => {
    loadFavoriteStatus()
    loadFollowingStatus()
  }
)
</script>

<style>
.neo-card {
  background: white;
  border: 4px solid black;
  box-shadow: 10px 10px 0px black;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(-1deg);
}

.rich-content h2 {
  font-size: 2rem;
  font-weight: 900;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-family: 'ZCOOL KuaiLe';
}

.rich-content p {
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  line-height: 1.8;
  font-weight: 600;
}

.rich-content blockquote {
  border-left: 8px solid var(--primary);
  padding-left: 1.5rem;
  font-style: italic;
  background: #fff5f5;
  padding: 1rem 1.5rem;
  border-radius: 0 20px 20px 0;
  margin: 2rem 0;
}
</style>
