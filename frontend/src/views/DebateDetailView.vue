<template>
  <div class="text-slate-900 pb-20 md:pb-0">
    <FloatingNav />
    <MainNav />

    <header class="bg-black text-white py-16 px-6 relative overflow-hidden">
      <div class="max-w-5xl mx-auto relative z-10 text-center">
        <div
          :class="[
            'inline-flex items-center gap-2 px-4 py-1 border-2 border-white rounded-full text-xs font-black uppercase mb-6 rotate-[-2deg]',
            topicOpen ? 'bg-pink-500 text-white' : 'bg-slate-600 text-white'
          ]"
        >
          {{ topicStatusLabel }}
        </div>
        <h1 class="text-4xl md:text-6xl font-black mb-8 leading-tight humor-font">
          {{ topic?.title || '话题加载中...' }}
        </h1>
        <div class="max-w-3xl mx-auto mt-12">
          <div class="bg-white/20 h-16 rounded-3xl border-4 border-white p-1">
            <div class="h-full rounded-2xl overflow-hidden flex">
              <button
                class="bg-[var(--accent)] h-full flex items-center justify-start px-6 text-white font-black text-base md:text-xl progress-arm min-w-0 focus:outline-none focus-visible:ring-4 focus-visible:ring-white/40"
                :style="{ width: `${percentA}%` }"
                :disabled="voting || !topicId || !topicOpen"
                type="button"
                aria-label="点击投票：正方"
                @click="voteFromBar('A')"
              >
                <span class="truncate">正方: {{ topic?.side_a_name || '正方' }} ({{ percentA }}%)</span>
              </button>
              <button
                class="bg-pink-500 h-full flex items-center justify-end px-6 text-white font-black text-base md:text-xl progress-arm min-w-0 focus:outline-none focus-visible:ring-4 focus-visible:ring-white/40"
                :style="{ width: `${percentB}%` }"
                :disabled="voting || !topicId || !topicOpen"
                type="button"
                aria-label="点击投票：反方"
                @click="voteFromBar('B')"
              >
                <span class="truncate">({{ percentB }}%) 反方: {{ topic?.side_b_name || '反方' }}</span>
              </button>
            </div>
          </div>
          <div class="mt-4 flex flex-wrap items-center justify-center gap-3 text-xs font-black">
            <span class="px-3 py-1 bg-white border-2 border-white rounded-full text-black">
              总票数：{{ voteTotal }}
            </span>
            <span class="px-3 py-1 bg-white border-2 border-white rounded-full text-black">
              正方：{{ votesA }} 票
            </span>
            <span class="px-3 py-1 bg-white border-2 border-white rounded-full text-black">
              反方：{{ votesB }} 票
            </span>
            <span v-if="myVoteSide" class="px-3 py-1 bg-yellow-400 border-2 border-white rounded-full text-black">
              你已投：{{ myVoteSide === 'A' ? '正方' : '反方' }}
            </span>
          </div>
        </div>
        <div class="mt-8 flex justify-center gap-4">
          <div class="flex flex-wrap items-center justify-center gap-3">
            <button
              class="px-6 py-3 rounded-2xl border-4 border-white font-black bouncy-btn disabled:opacity-50"
              :class="myVoteSide === 'A' ? 'bg-[var(--accent)] text-white' : 'bg-white text-black'"
              :disabled="voting || !topicId || !topicOpen"
              type="button"
              @click="vote('A')"
            >
              👍 投正方
            </button>
            <button
              class="px-6 py-3 rounded-2xl border-4 border-white font-black bouncy-btn disabled:opacity-50"
              :class="myVoteSide === 'B' ? 'bg-pink-500 text-white' : 'bg-white text-black'"
              :disabled="voting || !topicId || !topicOpen"
              type="button"
              @click="vote('B')"
            >
              👎 投反方
            </button>
          </div>
          <button
            class="bg-white text-black px-6 py-3 rounded-2xl border-4 border-white font-black bouncy-btn"
            type="button"
            @click="toggleFavorite"
          >
            {{ isFavorited ? '💔 取消收藏' : '🔖 收藏' }}
          </button>
        </div>
        <div v-if="voteError" class="mt-4 max-w-xl mx-auto bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
          {{ voteError }}
        </div>
        <div v-if="topicActionError" class="mt-4 max-w-xl mx-auto bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
          {{ topicActionError }}
        </div>
        <div v-if="isTopicCreator && topic" class="mt-8 flex flex-wrap justify-center gap-3">
          <button
            v-if="topicOpen"
            class="bg-yellow-400 text-black px-5 py-2 rounded-2xl border-4 border-white font-black text-sm bouncy-btn"
            type="button"
            @click="closeTopic"
          >
            收起话题
          </button>
          <button
            v-if="topic?.status === 'closed'"
            class="bg-mint text-black px-5 py-2 rounded-2xl border-4 border-white font-black text-sm bouncy-btn"
            type="button"
            @click="reopenTopic"
          >
            重新打开
          </button>
          <button
            v-if="topic?.status === 'open' || topic?.status === 'closed'"
            class="bg-white/20 text-white px-5 py-2 rounded-2xl border-4 border-white font-black text-sm bouncy-btn"
            type="button"
            @click="archiveTopic"
          >
            归档
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-12 grid grid-cols-1 lg:grid-cols-4 gap-10">
      <aside class="lg:col-span-1 space-y-8">
        <div class="neo-bubble p-6 bg-yellow-300">
          <h4 class="font-black text-xl mb-4 humor-font">🪧 抬杠规则</h4>
          <ul class="space-y-3 text-sm font-bold">
            <li class="flex items-center gap-2"><Icon class="text-black" icon="mdi:check-circle"></Icon> 不准人身攻击 (除非你是说自己)</li>
            <li class="flex items-center gap-2"><Icon class="text-black" icon="mdi:check-circle"></Icon> 证据要像奶茶一样有料</li>
            <li class="flex items-center gap-2"><Icon class="text-black" icon="mdi:check-circle"></Icon> 逻辑崩了可以撒娇求饶</li>
          </ul>
        </div>
        <div class="neo-bubble p-6 bg-mint">
          <h4 class="font-black text-xl mb-4 humor-font">🍭 核心梗概</h4>
          <p class="text-sm font-bold leading-relaxed">
            {{ topic?.description || '暂无描述' }}
          </p>
        </div>
      </aside>

      <section class="lg:col-span-3 space-y-12">
        <div v-if="errorMsg" class="neo-bubble p-6 bg-red-100">
          <p class="font-black text-red-700">{{ errorMsg }}</p>
        </div>

        <div class="space-y-16 py-8">
          <div v-for="p in topLevelPosts" :key="p.id" :class="['flex gap-4 items-start', p.side === 'B' ? 'flex-row-reverse' : '']">
            <div
              :class="[
                'w-20 h-20 border-4 border-black rounded-3xl flex-shrink-0 flex items-center justify-center text-white shadow-[4px_4px_0px_black]',
                p.side === 'A' ? 'bg-[var(--accent)] transform rotate-[-5deg]' : 'bg-pink-500 transform rotate-[5deg]'
              ]"
            >
              <Icon :icon="p.side === 'A' ? 'mdi:alien-outline' : 'mdi:ghost'" width="40"></Icon>
            </div>
            <div class="neo-bubble flex-1 p-8">
              <div class="flex items-center gap-4 mb-4">
                <span class="font-black text-xl">{{ p.user?.username || '匿名杠精' }}</span>
                <span
                  :class="[
                    'text-xs font-black px-2 py-1 border rounded',
                    p.side === 'A'
                      ? 'bg-[color:var(--accent)]/20 text-[var(--accent)] border-[var(--accent)]'
                      : 'bg-pink-500/20 text-pink-600 border-pink-500'
                  ]"
                >
                  {{ p.side === 'A' ? '正方' : '反方' }}
                </span>
                <span class="text-xs font-black text-slate-400">{{ formatDateTime(p.created_at) }}</span>
              </div>
              <p class="text-lg font-bold leading-relaxed mb-6">
                {{ p.content }}
              </p>
              <div v-if="p.evidence_url" :class="['flex gap-4', p.side === 'B' ? 'justify-end' : '']">
                <a class="bg-yellow-200 border-2 border-black px-4 py-2 rounded-xl text-sm font-black hover:bg-yellow-400 transition-colors" :href="p.evidence_url" target="_blank">
                  🍬 证据链接
                </a>
              </div>
              <div :class="['mt-6 flex items-center justify-between gap-3 flex-wrap', p.side === 'B' ? 'flex-row-reverse' : '']">
                <div :class="['flex items-center gap-2 flex-wrap', p.side === 'B' ? 'flex-row-reverse' : '']">
                  <button
                    class="px-4 py-2 border-4 border-black rounded-2xl font-black text-sm bouncy-btn bg-white hover:bg-yellow-300 disabled:opacity-50"
                    type="button"
                    :disabled="!topicOpen"
                    @click="openReply(p)"
                  >
                    💬 回复
                  </button>
                  <button
                    v-if="canDeleteDebatePost(p)"
                    class="px-4 py-2 border-4 border-red-600 text-red-700 rounded-2xl font-black text-sm bouncy-btn bg-white hover:bg-red-50"
                    type="button"
                    @click="deleteDebatePost(p)"
                  >
                    删除
                  </button>
                </div>
                <span class="text-xs font-black text-slate-400">{{ repliesByParent[p.id]?.length ? `回复 ${repliesByParent[p.id].length}` : '还没人回怼' }}</span>
              </div>

              <div v-if="replyingToId === p.id" class="mt-6 neo-bubble p-4 bg-slate-50">
                <div class="flex items-center justify-between gap-4 mb-3">
                  <p class="font-black text-sm">
                    回复 @{{ p.user?.username || '匿名' }}
                    <span class="ml-2 text-xs text-slate-500 font-bold">({{ p.side === 'A' ? '正方' : '反方' }})</span>
                  </p>
                  <button class="text-xs font-black underline" type="button" @click="cancelReply">取消</button>
                </div>
                <input
                  v-model="replyText"
                  class="w-full px-4 py-3 border-4 border-black rounded-2xl font-black bg-white focus:outline-none disabled:opacity-50"
                  placeholder="写点有理有据（或者无理取闹）的回复..."
                  type="text"
                  :disabled="!topicOpen"
                  @keyup.enter="submitReply()"
                />
                <div class="mt-3 flex items-center justify-between gap-3">
                  <p v-if="replyError" class="text-sm font-black text-red-600">{{ replyError }}</p>
                  <div class="flex items-center gap-3 ml-auto">
                    <button
                      class="bg-black text-white px-4 py-2 rounded-2xl border-4 border-black font-black bouncy-btn disabled:opacity-50"
                      :disabled="replyPosting || !replyText.trim() || !topicOpen"
                      type="button"
                      @click="submitReply()"
                    >
                      <span class="inline-flex items-center gap-2"><Icon icon="mdi:reply" width="18"></Icon> 回怼</span>
                    </button>
                  </div>
                </div>
              </div>

              <div v-if="repliesByParent[p.id]?.length" class="mt-6 space-y-4">
                <div v-for="r in repliesByParent[p.id]" :key="r.id" :id="`post-${r.id}`" class="neo-bubble p-4 bg-slate-50">
                  <div class="flex items-center gap-3 mb-2">
                    <img
                      class="w-8 h-8 rounded-full border-4 border-black bg-white flex-shrink-0"
                      :src="userAvatarUrl(r.user)"
                      :alt="r.user?.username || '匿名'"
                      loading="lazy"
                    />
                    <span class="font-black">@{{ r.user?.username || '匿名' }}</span>
                    <span class="text-xs font-black text-slate-400">{{ formatDateTime(r.created_at) }}</span>
                  </div>
                  <p class="font-bold text-slate-700">{{ r.content }}</p>
                  <div v-if="canDeleteDebatePost(r)" class="mt-3 flex justify-end">
                    <button
                      class="px-3 py-1 border-2 border-red-600 text-red-700 rounded-xl font-black text-xs bouncy-btn bg-white"
                      type="button"
                      @click="deleteDebatePost(r)"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="!topLevelPosts.length && !errorMsg" class="neo-bubble p-8 bg-white text-center">
            <p class="font-black text-slate-500">还没有人开喷，快来当第一口。</p>
          </div>
        </div>

        <div class="bg-white border-8 border-black p-6 rounded-[40px] shadow-[12px_12px_0px_black] flex items-start gap-6">
          <div class="flex flex-col items-center gap-2 w-20">
            <img alt="me" class="w-16 h-16 rounded-full border-4 border-black" :src="myAvatarUrl" />
            <p class="text-xs font-black text-center break-words w-full">{{ auth.user?.username || '我' }}</p>
          </div>
          <div class="flex-1">
            <input
              v-model="composerText"
              class="w-full text-2xl font-black bg-transparent focus:outline-none placeholder:text-slate-300 disabled:opacity-50"
              placeholder="输入你的神逻辑，震惊全场..."
              type="text"
              :disabled="!topicOpen"
              @keyup.enter="submitPost()"
            />
            <div class="mt-4 flex flex-wrap items-center justify-between gap-3">
              <div class="flex items-center gap-2">
                <button
                  class="px-4 py-2 border-4 border-black rounded-2xl font-black text-sm bouncy-btn disabled:opacity-50"
                  :class="composerSide === 'A' ? 'bg-[var(--accent)] text-white' : 'bg-white text-black'"
                  type="button"
                  :disabled="!topicOpen"
                  @click="composerSide = 'A'"
                >
                  正方
                </button>
                <button
                  class="px-4 py-2 border-4 border-black rounded-2xl font-black text-sm bouncy-btn disabled:opacity-50"
                  :class="composerSide === 'B' ? 'bg-pink-500 text-white' : 'bg-white text-black'"
                  type="button"
                  :disabled="!topicOpen"
                  @click="composerSide = 'B'"
                >
                  反方
                </button>
              </div>
              <div class="flex items-center gap-3">
                <button
                  v-if="autoMode"
                  class="bg-black text-white px-5 py-2 rounded-2xl border-4 border-black font-black bouncy-btn disabled:opacity-50"
                  :disabled="posting || !topicOpen"
                  type="button"
                  @click="autoSend"
                >
                  🤖 一键抬杠
                </button>
                <button
                  class="bg-yellow-400 border-4 border-black px-5 py-2 rounded-2xl bouncy-btn shadow-[4px_4px_0px_black] font-black disabled:opacity-50"
                  :disabled="posting || !composerText.trim() || !topicOpen"
                  type="button"
                  @click="submitPost()"
                >
                  <span class="inline-flex items-center gap-2"><Icon icon="mdi:send-variant" width="22"></Icon> 发射</span>
                </button>
              </div>
            </div>
            <div v-if="composerError" class="mt-4 bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
              {{ composerError }}
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="bg-black py-12 mt-20 text-white">
      <div class="max-w-7xl mx-auto px-6 text-center">
        <p class="font-black text-xl humor-font mb-4">思辩乐园 - 把脑洞开到底</p>
        <p class="text-slate-400 font-bold">© 2026 辩论虽好，可不要贪杯哦（指吵到凌晨三点）。</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import FloatingNav from '../components/layout/FloatingNav.vue'
import MainNav from '../components/layout/MainNav.vue'
import { http } from '../api/http'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const topic = ref(null)
const posts = ref([])
const errorMsg = ref('')

const topicId = computed(() => {
  const v = route.query.id || route.query.topicId
  const id = Number(v || 0)
  return Number.isFinite(id) ? id : 0
})

const votesA = computed(() => topic.value?.votes?.A || 0)
const votesB = computed(() => topic.value?.votes?.B || 0)
const voteTotal = computed(() => votesA.value + votesB.value)

const percentA = computed(() => {
  if (!voteTotal.value) return 50
  return Math.round((votesA.value / voteTotal.value) * 100)
})
const percentB = computed(() => 100 - percentA.value)


const repliesByParent = computed(() => {
  const map = {}
  for (const p of posts.value) {
    if (!p.parent_id) continue
    map[p.parent_id] = map[p.parent_id] || []
    map[p.parent_id].push(p)
  }
  return map
})

const topLevelPosts = computed(() => posts.value.filter((p) => !p.parent_id))

/** 未拉到 topic 前必须为 false，避免误开投票/发帖与错误状态文案 */
const topicOpen = computed(() => !!topic.value && (topic.value.status || 'open') === 'open')
const topicStatusLabel = computed(() => {
  if (!topic.value) return '加载中…'
  const s = topic.value.status || 'open'
  if (s === 'open') return '🔥 战况焦灼中…'
  if (s === 'closed') return '🧊 话题已收起'
  return '📦 已归档'
})
const topicActionError = ref('')
const isTopicCreator = computed(
  () => !!(auth.user?.id && topic.value?.creator?.id && auth.user.id === topic.value.creator.id)
)

const isFavorited = ref(false)
const myVoteSide = ref('')
const voting = ref(false)
const voteError = ref('')
const composerText = ref('')
const composerSide = ref('A')
const posting = ref(false)
const composerError = ref('')
const replyingToId = ref(0)
const replyText = ref('')
const replyPosting = ref(false)
const replyError = ref('')

const autoMode = computed(() => !!auth.user?.auto_debate_mode)
const myAvatarUrl = computed(
  () => auth.user?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(auth.user?.username || 'me')}`
)

const userAvatarUrl = (user) => {
  const url = user?.avatar_url
  if (url) return url
  const seed = user?.username || `u${user?.id || ''}` || 'anon'
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(seed)}`
}

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

const patchTopicMeta = async (payload) => {
  topicActionError.value = ''
  if (!topicId.value) return
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  try {
    const r = await http.patch(`topics/${topicId.value}/`, payload)
    if (r?.item) topic.value = r.item
  } catch (e) {
    topicActionError.value = e?.message || '操作失败'
  }
}

const closeTopic = () => patchTopicMeta({ status: 'closed' })
const reopenTopic = () => patchTopicMeta({ status: 'open' })
const archiveTopic = () => {
  if (!window.confirm('归档后无法再修改话题，确定？')) return
  patchTopicMeta({ status: 'archived' })
}

const canDeleteDebatePost = (p) => {
  if (!auth.isAuthed || !topicOpen.value || !p) return false
  if (p.user?.id !== auth.user.id) return false
  return !(repliesByParent.value[p.id]?.length > 0)
}

const deleteDebatePost = async (p) => {
  if (!canDeleteDebatePost(p)) return
  if (!window.confirm('确定删除该观点？')) return
  topicActionError.value = ''
  try {
    await http.delete(`topics/${topicId.value}/posts/${p.id}/`)
    posts.value = posts.value.filter((x) => x.id !== p.id)
    if (topic.value && Number.isFinite(Number(topic.value.comment_count))) {
      topic.value = { ...topic.value, comment_count: Math.max(0, Number(topic.value.comment_count) - 1) }
    }
  } catch (e) {
    topicActionError.value = e?.message || '删除失败'
  }
}

const loadTopic = async () => {
  errorMsg.value = ''
  topic.value = null
  posts.value = []
  if (!topicId.value) {
    errorMsg.value = '缺少话题 id'
    return
  }
  try {
    const [t, r] = await Promise.all([http.get(`topics/${topicId.value}/`), http.get(`topics/${topicId.value}/posts/`)])
    topic.value = t?.item || null
    posts.value = r?.items || []
    myVoteSide.value = String(topic.value?.my_vote || '')
  } catch (e) {
    errorMsg.value = e?.message || '加载失败'
  }
}

const loadMyVote = async () => {
  myVoteSide.value = ''
  if (!auth.isAuthed || !topicId.value) return
  try {
    const r = await http.get(`topics/${topicId.value}/vote/`)
    myVoteSide.value = String(r?.side || '')
  } catch {
    myVoteSide.value = ''
  }
}

const vote = async (side) => {
  voteError.value = ''
  if (!topicId.value) return
  if (!topicOpen.value) {
    voteError.value = '话题已关闭，无法投票'
    return
  }
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  if (myVoteSide.value) {
    voteError.value = '你已投过票啦'
    return
  }
  const s = String(side || '').toUpperCase()
  if (s !== 'A' && s !== 'B') return
  if (voting.value) return
  voting.value = true
  try {
    await http.post(`topics/${topicId.value}/vote/`, { side: s })
    myVoteSide.value = s
    await loadTopic().catch(() => {})
  } catch (e) {
    const msg = e?.message || '投票失败'
    voteError.value = msg.includes('已投票') ? '你已投过票啦' : msg
    await loadMyVote().catch(() => {})
  } finally {
    voting.value = false
  }
}

const voteFromBar = (side) => {
  vote(side)
}

const loadFavoriteStatus = async () => {
  isFavorited.value = false
  if (!auth.isAuthed || !topicId.value) return
  try {
    const r = await http.get('favorites/status/', { params: { target_type: 'topic', target_id: topicId.value } })
    isFavorited.value = !!r?.is_favorited
  } catch {
    isFavorited.value = false
  }
}

const toggleFavorite = async () => {
  if (!topicId.value) return
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  if (isFavorited.value) {
    await http.delete('favorites/', { params: { target_type: 'topic', target_id: topicId.value } })
  } else {
    await http.post('favorites/', { target_type: 'topic', target_id: topicId.value })
  }
  await loadFavoriteStatus()
}

const genAutoText = () => {
  const title = topic.value?.title || '这个话题'
  const a = topic.value?.side_a_name || '正方'
  const b = topic.value?.side_b_name || '反方'
  const sideName = composerSide.value === 'A' ? a : b
  const pool = [
    `我站 ${sideName}：${title} 这题核心不是对错，是谁更会讲人话。`,
    `先声明我站 ${sideName}。你们说得都很有道理，但我更喜欢我的道理。`,
    `关于「${title}」我只说一句：${sideName} 这边至少逻辑闭环了。`,
    `如果把这个话题当成 bug 来修，${sideName} 这边至少给了可复现步骤。`,
    `别急着反驳，先承认我站 ${sideName} 比你站得更稳。`
  ]
  return pool[Math.floor(Math.random() * pool.length)]
}

const submitPost = async (contentOverride) => {
  composerError.value = ''
  if (!topicOpen.value) {
    composerError.value = '话题已关闭，无法发表'
    return
  }
  const content = String(contentOverride ?? composerText.value ?? '').trim()
  if (!content) {
    composerError.value = '先写点东西再发射'
    return
  }
  if (!topicId.value) return
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  posting.value = true
  try {
    await http.post(`topics/${topicId.value}/posts/`, { side: composerSide.value, content })
    composerText.value = ''
    await loadTopic()
  } catch (e) {
    composerError.value = e?.message || '发送失败'
  } finally {
    posting.value = false
  }
}

const openReply = (p) => {
  replyError.value = ''
  const id = Number(p?.id || 0)
  if (!id) return
  replyingToId.value = id
  replyText.value = ''
}

const cancelReply = () => {
  replyingToId.value = 0
  replyText.value = ''
  replyError.value = ''
}

const submitReply = async () => {
  replyError.value = ''
  if (!topicOpen.value) {
    replyError.value = '话题已关闭，无法回复'
    return
  }
  const content = String(replyText.value || '').trim()
  if (!content) {
    replyError.value = '先写点东西再回怼'
    return
  }
  if (!topicId.value) return
  const parentId = Number(replyingToId.value || 0)
  if (!parentId) return
  if (!auth.isAuthed) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  if (replyPosting.value) return
  replyPosting.value = true
  try {
    const parent = posts.value.find((x) => x.id === parentId)
    const side = parent?.side || composerSide.value || 'A'
    const r = await http.post(`topics/${topicId.value}/posts/`, { side, content, parent_id: parentId })
    const item = r?.item
    const newId = Number(item?.id || 0)
    if (item && newId) {
      const next = { ...item }
      const lastIdx = posts.value.reduce((acc, p, i) => (p?.parent_id === parentId ? i : acc), -1)
      if (lastIdx >= 0) posts.value.splice(lastIdx + 1, 0, next)
      else posts.value.push(next)
      if (topic.value && Number.isFinite(Number(topic.value.comment_count))) {
        topic.value = { ...topic.value, comment_count: Number(topic.value.comment_count) + 1 }
      }
      cancelReply()
      await nextTick()
      const el = document.getElementById(`post-${newId}`)
      if (el && typeof el.scrollIntoView === 'function') el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    } else {
      cancelReply()
      await loadTopic()
    }
  } catch (e) {
    replyError.value = e?.message || '回复失败'
  } finally {
    replyPosting.value = false
  }
}

const autoSend = async () => {
  const content = genAutoText()
  composerText.value = content
  await submitPost(content)
}

watch(
  () => topicId.value,
  () => {
    loadTopic()
    loadFavoriteStatus()
    loadMyVote()
  },
  { immediate: true }
)

watch(
  () => auth.isAuthed,
  () => {
    loadFavoriteStatus()
    loadMyVote()
  }
)
</script>

<style>
.neo-bubble {
  background: white;
  border: 4px solid black;
  box-shadow: 6px 6px 0px black;
  border-radius: 24px;
  position: relative;
}

.neo-bubble::after {
  content: '';
  position: absolute;
  width: 0;
  height: 0;
  border-left: 15px solid transparent;
  border-right: 15px solid transparent;
  border-top: 15px solid black;
  bottom: -15px;
  left: 30px;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(-1deg);
}

.progress-arm {
  transition: width 1s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.float-icon {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
</style>
