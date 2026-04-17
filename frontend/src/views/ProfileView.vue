<template>
  <div class="pb-24 md:pb-0">
    <nav class="sticky top-0 z-50 bg-white border-b-4 border-black px-6 py-4">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <RouterLink class="text-3xl font-black humor-font flex items-center gap-2 group" to="/">
          <span class="bg-pink-500 text-white p-2 border-2 border-black shadow-[4px_4px_0px_black] group-hover:rotate-12 transition-transform">思</span>
          <span class="bg-blue-500 text-white p-2 border-2 border-black shadow-[4px_4px_0px_black] group-hover:-rotate-12 transition-transform">辨</span>
          <span class="text-black ml-2">乐园</span>
        </RouterLink>
        <div class="flex items-center gap-6">
          <RouterLink class="font-black hover:text-pink-600" to="/debate-list">广场</RouterLink>
          <RouterLink class="font-black hover:text-blue-600" to="/tournament">联赛</RouterLink>
          <div class="relative group">
            <div class="w-12 h-12 bg-secondary border-4 border-black rounded-full overflow-hidden cursor-pointer shadow-[4px_4px_0px_black]">
              <img :src="avatarUrlSmall" alt="avatar" />
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="fixed md:right-8 bottom-4 left-4 right-4 md:left-auto md:top-1/2 md:-translate-y-1/2 z-50 flex md:flex-column flex-row justify-center gap-4">
      <div class="flex md:flex-col gap-4 bg-white/80 backdrop-blur p-3 border-4 border-black rounded-3xl shadow-[8px_8px_0px_black]">
        <button
          :class="tabBtnClass('overview', 'hover:bg-yellow-300')"
          data-tab="overview"
          type="button"
          @click="switchTab('overview')"
        >
          <Icon class="text-2xl" icon="mdi:view-dashboard"></Icon>
        </button>
        <button :class="tabBtnClass('timeline', 'hover:bg-blue-300')" data-tab="timeline" type="button" @click="switchTab('timeline')">
          <Icon class="text-2xl" icon="mdi:history"></Icon>
        </button>
        <button
          :class="tabBtnClass('community', 'hover:bg-green-300')"
          data-tab="community"
          type="button"
          @click="switchTab('community')"
        >
          <Icon class="text-2xl" icon="mdi:account-group"></Icon>
        </button>
        <button
          :class="tabBtnClass('favorites', 'hover:bg-purple-300')"
          data-tab="favorites"
          type="button"
          @click="switchTab('favorites')"
        >
          <Icon class="text-2xl" icon="mdi:bookmark"></Icon>
        </button>
        <button
          :class="tabBtnClass('messages', 'hover:bg-pink-300')"
          class="relative"
          data-tab="messages"
          type="button"
          @click="switchTab('messages')"
        >
          <Icon class="text-2xl" icon="mdi:message-text"></Icon>
          <div v-if="unreadCount" class="badge-dot">{{ unreadCount }}</div>
        </button>
        <button
          :class="tabBtnClass('settings', 'hover:bg-slate-300')"
          data-tab="settings"
          type="button"
          @click="switchTab('settings')"
        >
          <Icon class="text-2xl" icon="mdi:cog"></Icon>
        </button>
      </div>
    </div>

    <main class="max-w-7xl mx-auto px-6 py-12">
      <div class="neo-panel p-8 mb-12 bg-white relative overflow-hidden">
        <div class="absolute top-0 right-0 w-32 h-32 bg-yellow-400 border-l-4 border-b-4 border-black abstract-shape flex items-center justify-center rotate-12 -mr-8 -mt-8">
          <span class="font-black text-xl humor-font pt-8 pr-4">LV.99</span>
        </div>
        <div class="flex flex-col md:flex-row items-center gap-10">
          <div class="relative group">
            <div class="w-40 h-40 border-8 border-black rounded-full overflow-hidden shadow-[8px_8px_0px_black] group-hover:rotate-6 transition-transform">
              <img :src="avatarUrlLarge" alt="avatar" class="w-full h-full object-cover" />
            </div>
            <button class="absolute bottom-0 right-0 bg-pink-500 border-4 border-black p-2 rounded-full hover:scale-110 transition-transform" type="button" @click="pickAvatar">
              <Icon class="text-white text-xl" icon="mdi:camera"></Icon>
            </button>
          </div>
          <div class="flex-1 text-center md:text-left">
            <h1 class="text-5xl font-black humor-font mb-4 flex items-center justify-center md:justify-start gap-3">
              {{ user?.username || '未登录' }} <span class="text-lg bg-black text-white px-3 py-1 rounded-full">{{ user?.role || 'user' }}</span>
            </h1>
            <p class="text-xl font-bold text-slate-600 mb-6 italic">"{{ user?.bio || '这里应该写一句很中二的签名。' }}"</p>
            <div class="flex flex-wrap justify-center md:justify-start gap-4">
              <div class="bg-blue-100 border-2 border-black px-4 py-2 rounded-xl font-black flex items-center gap-2">
                <Icon icon="mdi:map-marker"></Icon> 逻辑荒原
              </div>
              <div class="bg-green-100 border-2 border-black px-4 py-2 rounded-xl font-black flex items-center gap-2">
                <Icon icon="mdi:cake"></Icon> {{ joinDateText }}
              </div>
              <button class="bouncy-btn bg-black text-white px-6 py-2 rounded-xl font-black" type="button" @click="refreshAll">刷新数据</button>
            </div>
          </div>
        </div>
      </div>

      <section v-show="activeTab === 'overview'" class="space-y-12" id="overview">
        <div class="grid grid-cols-2 md:grid-cols-5 gap-6">
          <div
            class="neo-panel p-6 bg-blue-400 text-white text-center group"
            :class="overviewStatClickable('topics_created') ? 'cursor-pointer' : 'cursor-default'"
            role="button"
            :tabindex="overviewStatClickable('topics_created') ? 0 : -1"
            :title="overviewStatTitle('topics_created')"
            @click="onOverviewStatClick('topics_created')"
            @keydown.enter.prevent="onOverviewStatClick('topics_created')"
            @keydown.space.prevent="onOverviewStatClick('topics_created')"
          >
            <div class="text-4xl font-black mb-1 group-hover:scale-125 transition-transform">{{ stats ? (hideWinRate ? '🤫' : statAnimated.topics_created) : '—' }}</div>
            <div class="font-bold text-sm">发起话题</div>
            <div class="text-[10px] mt-2 opacity-80">制造混乱的源头</div>
          </div>
          <div
            class="neo-panel p-6 bg-pink-400 text-white text-center group"
            :class="overviewStatClickable('debate_posts') ? 'cursor-pointer' : 'cursor-default'"
            role="button"
            :tabindex="overviewStatClickable('debate_posts') ? 0 : -1"
            :title="overviewStatTitle('debate_posts')"
            @click="onOverviewStatClick('debate_posts')"
            @keydown.enter.prevent="onOverviewStatClick('debate_posts')"
            @keydown.space.prevent="onOverviewStatClick('debate_posts')"
          >
            <div class="text-4xl font-black mb-1 group-hover:scale-125 transition-transform">{{ stats ? (hideWinRate ? '🤫' : statAnimated.debate_posts) : '—' }}</div>
            <div class="font-bold text-sm">观点数量</div>
            <div class="text-[10px] mt-2 opacity-80">输出的神逻辑总和</div>
          </div>
          <div
            class="neo-panel p-6 bg-yellow-400 text-black text-center group"
            :class="overviewStatClickable('blog_posts') ? 'cursor-pointer' : 'cursor-default'"
            role="button"
            :tabindex="overviewStatClickable('blog_posts') ? 0 : -1"
            :title="overviewStatTitle('blog_posts')"
            @click="onOverviewStatClick('blog_posts')"
            @keydown.enter.prevent="onOverviewStatClick('blog_posts')"
            @keydown.space.prevent="onOverviewStatClick('blog_posts')"
          >
            <div class="text-4xl font-black mb-1 group-hover:scale-125 transition-transform">{{ stats ? (hideWinRate ? '🤫' : statAnimated.blog_posts) : '—' }}</div>
            <div class="font-bold text-sm">博客文章</div>
            <div class="text-[10px] mt-2 opacity-80">码字机器人的修养</div>
          </div>
          <div class="neo-panel p-6 bg-purple-400 text-white text-center group cursor-default">
            <div class="text-4xl font-black mb-1">{{ stats ? (hideWinRate ? '🤫' : statAnimated.followers) : '—' }}</div>
            <div class="font-bold text-sm">粉丝数</div>
            <div class="text-[10px] mt-2 opacity-80">信徒分布在全宇宙</div>
          </div>
          <div
            class="neo-panel p-6 bg-mint text-black text-center group cursor-default"
            title="已发布博客点赞数 + 观点获赞（upvotes）之和"
          >
            <div class="text-4xl font-black mb-1 group-hover:scale-125 transition-transform">{{ stats ? (hideWinRate ? '🤫' : statAnimated.likes_total) : '—' }}</div>
            <div class="font-bold text-sm">获赞总数</div>
            <div class="text-[10px] mt-2 opacity-80">人类认可的虚荣心</div>
          </div>
        </div>

        <div v-reveal="50" class="neo-panel p-10 bg-white">
          <h3 class="text-3xl humor-font font-black mb-8 flex items-center gap-4">📚 我的作品集</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div id="profile-my-topics" class="neo-panel p-6 bg-slate-50 scroll-mt-28">
              <p class="font-black text-lg mb-4">我的话题</p>
              <div v-if="myTopics.length" class="space-y-3">
                <RouterLink
                  v-for="t in myTopics"
                  :key="t.id"
                  v-reveal="80"
                  class="block p-4 bg-white border-4 border-black rounded-2xl font-black hover:bg-yellow-100 transition-colors"
                  :to="{ path: '/debate-detail', query: { id: String(t.id) } }"
                >
                  <div class="text-xs text-slate-500 font-bold mb-1">{{ t.category }} · {{ formatDateTime(t.created_at) }}</div>
                  <div class="text-base">{{ t.title }}</div>
                </RouterLink>
              </div>
              <button v-else class="w-full text-left text-slate-500 font-bold hover:text-black transition-colors" type="button" @click="openPublishPrompt('topic')">
                还没发过话题，点我去发布
              </button>
            </div>

            <div id="profile-my-blogs" class="neo-panel p-6 bg-slate-50 scroll-mt-28">
              <p class="font-black text-lg mb-4">我的文章</p>
              <div v-if="myBlogPosts.length" class="space-y-3">
                <RouterLink
                  v-for="p in myBlogPosts"
                  :key="p.id"
                  v-reveal="80"
                  class="block p-4 bg-white border-4 border-black rounded-2xl font-black hover:bg-pink-100 transition-colors"
                  :to="{ path: '/blog-detail', query: { id: String(p.id), slug: p.slug || '' } }"
                >
                  <div class="text-xs text-slate-500 font-bold mb-1">{{ p.category }} · {{ formatDateTime(p.created_at) }}</div>
                  <div class="text-base">{{ p.title }}</div>
                </RouterLink>
              </div>
              <button v-else class="w-full text-left text-slate-500 font-bold hover:text-black transition-colors" type="button" @click="openPublishPrompt('blog')">
                还没发过文章，点我去发布
              </button>
            </div>

            <div id="profile-my-debates" class="neo-panel p-6 bg-slate-50 scroll-mt-28">
              <p class="font-black text-lg mb-4">我的观点</p>
              <div v-if="myDebatePosts.length" class="space-y-3">
                <RouterLink
                  v-for="p in myDebatePosts"
                  :key="p.id"
                  v-reveal="80"
                  class="block p-4 bg-white border-4 border-black rounded-2xl font-black hover:bg-blue-100 transition-colors"
                  :to="{ path: '/debate-detail', query: { id: String(p.topic_id) } }"
                >
                  <div class="text-xs text-slate-500 font-bold mb-1">{{ p.side }}方 · {{ formatDateTime(p.created_at) }}</div>
                  <div class="text-base mb-2">{{ p.topic_title }}</div>
                  <div class="text-sm text-slate-700 font-bold">{{ p.content }}</div>
                </RouterLink>
              </div>
              <button v-else class="w-full text-left text-slate-500 font-bold hover:text-black transition-colors" type="button" @click="goDebateList">
                还没发过观点，点我去话题池抬杠
              </button>
            </div>
          </div>
        </div>

        <div class="neo-panel p-10 bg-white">
          <h3 class="text-3xl humor-font font-black mb-8 flex items-center gap-4">🏆 荣誉废纸堆</h3>
          <div v-if="badges.length" class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-8">
            <div v-for="b in badges" :key="b.id" class="text-center group">
              <div
                class="w-24 h-24 bg-yellow-300 border-4 border-black rounded-full mx-auto flex items-center justify-center shadow-[6px_6px_0px_black] group-hover:rotate-12 transition-transform"
              >
                <img class="w-14 h-14" :src="badgeSrc(b.icon_id)" :alt="b.name" loading="lazy" />
              </div>
              <p class="font-black mt-4">{{ b.name }}</p>
              <p class="text-[10px] text-slate-500 font-bold">{{ b.description }}</p>
            </div>
          </div>
          <div v-else class="font-black text-slate-500">你还没有拿到徽章，先去发话题/写文章/抬杠试试！</div>
        </div>

        <div id="profile-heatmap" class="neo-panel p-10 bg-white scroll-mt-28">
          <div class="flex flex-col gap-2 md:flex-row md:justify-between md:items-center mb-6">
            <div>
              <h3 class="text-3xl humor-font font-black flex items-center gap-4">📅 码字心电图</h3>
              <p class="text-xs font-bold text-slate-500 mt-2">方格颜色 = 当日活动次数；点击某一天可跳到「时间线」并只显示该日记录（与心电图同源）。</p>
            </div>
            <div class="flex items-center gap-2 text-xs font-bold shrink-0">
              <span>少杠</span>
              <div class="w-3 h-3 level-0"></div>
              <div class="w-3 h-3 level-1"></div>
              <div class="w-3 h-3 level-2"></div>
              <div class="w-3 h-3 level-3"></div>
              <div class="w-3 h-3 level-4"></div>
              <span>狂杠</span>
            </div>
          </div>
          <div class="overflow-x-auto">
            <div class="heatmap-grid min-w-[1100px]">
              <div
                v-for="cell in heatmapCells"
                :key="cell.date"
                :title="heatmapCellTitle(cell)"
                role="button"
                tabindex="0"
                :class="[
                  'heatmap-cell',
                  `level-${cell.level}`,
                  'hover:border-black',
                  'cursor-pointer',
                  'transition-all',
                  'focus:outline-none',
                  'focus-visible:ring-4',
                  'focus-visible:ring-black/30'
                ]"
                @click="onHeatmapCellClick(cell)"
                @keydown.enter.prevent="onHeatmapCellClick(cell)"
                @keydown.space.prevent="onHeatmapCellClick(cell)"
              ></div>
            </div>
          </div>
          <p class="mt-4 text-slate-500 font-bold italic text-sm text-right">过去12个月，你一共杠了 {{ heatmapTotal }} 次。</p>
        </div>
      </section>

      <section v-show="activeTab === 'timeline'" class="space-y-8" id="timeline">
        <div class="neo-panel p-10 bg-white relative">
          <h3 class="text-3xl humor-font font-black mb-8 flex items-center gap-4">🕰️ 犯罪现场记录</h3>
          <div
            v-if="activityFilterDate"
            class="mb-8 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between rounded-2xl border-4 border-black bg-yellow-100 px-4 py-3"
          >
            <p class="font-black text-sm sm:text-base">
              正在查看 <span class="text-pink-600">{{ activityFilterDateLabel }}</span> 的记录（按本地日历日与心电图对齐）
            </p>
            <button
              class="bouncy-btn shrink-0 bg-black text-white px-4 py-2 rounded-xl font-black text-sm"
              type="button"
              @click="clearActivityDayFilter"
            >
              显示全部
            </button>
          </div>
          <div class="relative pl-12 space-y-12">
            <div v-if="displayActivityItems.length" class="timeline-line"></div>
            <div v-for="item in displayActivityItems" :key="item.id" class="relative">
              <div :class="['absolute -left-[54px] top-0 w-8 h-8 border-4 border-black rounded-full z-10', activityDotClass(item.action_type)]"></div>
              <button class="neo-panel p-6 bg-white transition-colors hover:bg-slate-50 text-left w-full" type="button" @click="openActivity(item)">
                <div class="flex justify-between mb-2">
                  <span class="text-sm font-black text-slate-400">{{ formatDateTime(item.created_at) }}</span>
                  <span :class="['text-white px-2 py-0.5 border-2 border-black text-[10px] font-black', activityTagClass(item.action_type)]">
                    {{ activityLabel(item.action_type) }}
                  </span>
                </div>
                <h4 class="text-xl font-black mb-2">{{ activityTitle(item) }}</h4>
                <p v-if="activityDesc(item)" class="font-bold text-slate-600">{{ activityDesc(item) }}</p>
              </button>
            </div>
            <p v-if="!displayActivityItems.length" class="font-black text-slate-500 pl-2 pr-2">
              <template v-if="activityFilterDate">
                这一天还没有出现在已加载的时间线里。若心电图显示有活动，可先点「显示全部」再点「加载更多」向后翻找。
              </template>
              <template v-else>暂无活动记录，去广场或博客搞点事情再来？</template>
            </p>
            <button
              v-if="activityHasMore"
              class="w-full py-4 border-4 border-dashed border-black rounded-2xl font-black hover:bg-black hover:text-white transition-all disabled:opacity-50"
              type="button"
              :disabled="loadingMoreActivity"
              @click="loadMoreTimeline"
            >
              {{ activityFilterDate ? '加载更多（向后翻找该日记录）' : '查看更早的历史记录 (或者干脆忘掉它们)' }}
            </button>
          </div>
        </div>
      </section>

      <section v-show="activeTab === 'community'" class="space-y-12" id="community">
        <div class="flex flex-col md:flex-row gap-8">
          <div class="flex-1 space-y-6">
            <h3 class="text-3xl humor-font font-black flex items-center gap-4 p-2 bg-yellow-300 border-4 border-black inline-block transform -rotate-2">
              👀 我的受害者 ({{ followingItems.length }})
            </h3>
            <div v-for="u in followingItems" :key="u.id" class="neo-panel p-4 flex items-center justify-between group">
              <div class="flex items-center gap-4">
                <div class="w-14 h-14 border-4 border-black rounded-xl overflow-hidden group-hover:rotate-6 transition-transform bg-white">
                  <img :src="u.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(u.username)}`" alt="avatar" />
                </div>
                <div>
                  <p class="font-black text-lg">@{{ u.username }}</p>
                  <p class="text-xs text-slate-500 font-bold">{{ u.bio || '该用户暂无简介' }}</p>
                </div>
              </div>
              <button class="bouncy-btn bg-black text-white px-4 py-2 rounded-xl font-black text-sm" type="button" @click="unfollow(u.id)">取消关注</button>
            </div>
          </div>
          <div class="flex-1 space-y-6">
            <h3 class="text-3xl humor-font font-black flex items-center gap-4 p-2 bg-pink-400 border-4 border-black inline-block transform rotate-2">
              💖 我的信徒 ({{ followersItems.length }})
            </h3>
            <div v-for="u in followersItems" :key="u.id" class="neo-panel p-4 flex items-center justify-between group">
              <div class="flex items-center gap-4">
                <div class="w-14 h-14 border-4 border-black rounded-xl overflow-hidden group-hover:-rotate-6 transition-transform bg-white">
                  <img :src="u.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(u.username)}`" alt="avatar" />
                </div>
                <div>
                  <p class="font-black text-lg">@{{ u.username }}</p>
                  <p class="text-xs text-slate-500 font-bold">{{ u.bio || '该用户暂无简介' }}</p>
                </div>
              </div>
              <button
                v-if="!followingIdSet.has(u.id) && u.id !== user?.id"
                class="bouncy-btn bg-pink-500 text-white px-4 py-2 rounded-xl font-black text-sm"
                type="button"
                @click="follow(u.id)"
              >
                回关
              </button>
              <div v-else class="px-4 py-2 rounded-xl font-black text-sm border-4 border-black bg-white">已关注</div>
            </div>
          </div>
        </div>
      </section>

      <section v-show="activeTab === 'favorites'" class="space-y-8" id="favorites">
        <div class="neo-panel p-10 bg-white">
          <h3 class="text-3xl humor-font font-black mb-8 flex items-center gap-4">🔖 我的珍藏歪理</h3>
          <div v-if="favoriteItems.length" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="f in favoriteItems" :key="f.id" class="relative">
              <RouterLink class="neo-panel p-6 bg-yellow-50 hover:bg-yellow-100 transition-colors block" :to="favoriteTo(f)">
                <p class="text-sm font-black text-slate-400 mb-2">收藏 · {{ favoriteTypeText(f.target_type) }}</p>
                <p class="text-xl font-black">{{ favoriteTitle(f) }}</p>
              </RouterLink>
              <button
                class="absolute top-4 right-4 w-10 h-10 rounded-full border-4 border-black bg-white font-black bouncy-btn"
                type="button"
                title="取消收藏"
                @click.stop.prevent="removeFavorite(f)"
              >
                ×
              </button>
            </div>
          </div>
          <div v-else class="font-black text-slate-500">还没有收藏，去话题池/胡说八道逛逛？</div>
          <button
            v-if="favoritesHasMore"
            class="mt-8 w-full py-4 border-4 border-dashed border-black rounded-2xl font-black hover:bg-black hover:text-white transition-all disabled:opacity-50"
            type="button"
            :disabled="loadingMoreFavorites"
            @click="loadMoreFavorites"
          >
            再翻点珍藏
          </button>
        </div>
      </section>

      <section v-show="activeTab === 'messages'" class="space-y-8" id="messages">
        <div class="neo-panel p-10 bg-white">
          <div class="flex items-center justify-between mb-8">
            <h3 class="text-3xl humor-font font-black flex items-center gap-4">💌 通知中心</h3>
            <button class="bouncy-btn bg-black text-white px-4 py-2 rounded-xl font-black text-sm" type="button" @click="markAllRead">全部已读</button>
          </div>
          <div v-if="notificationItems.length" class="space-y-4">
            <div
              v-for="n in notificationItems"
              :key="n.id"
              :class="['neo-panel p-6 transition-colors', n.is_read ? 'bg-white hover:bg-slate-50' : 'bg-pink-50 hover:bg-pink-100']"
              @click="openNotification(n)"
            >
              <div class="flex justify-between items-center mb-2">
                <p class="font-black text-lg">{{ notificationTitle(n) }}</p>
                <span class="text-xs font-black text-slate-400">{{ formatDateTime(n.created_at) }}</span>
              </div>
              <p class="font-bold text-slate-600">{{ notificationBody(n) }}</p>
              <div class="mt-3 flex justify-end">
                <button v-if="!n.is_read" class="bouncy-btn bg-black text-white px-3 py-2 rounded-xl font-black text-xs" type="button" @click.stop="markRead(n.id)">
                  标记已读
                </button>
              </div>
            </div>
          </div>
          <div v-else class="font-black text-slate-500">暂无通知，世界清净得有点不习惯。</div>
          <button
            v-if="notificationsHasMore"
            class="mt-8 w-full py-4 border-4 border-dashed border-black rounded-2xl font-black hover:bg-black hover:text-white transition-all disabled:opacity-50"
            type="button"
            :disabled="loadingMoreNotifications"
            @click="loadMoreNotifications"
          >
            加载更多通知
          </button>
          <p v-if="quickReplyHint" class="mt-6 text-sm font-black text-slate-600">{{ quickReplyHint }}</p>
          <p v-if="autoDebateMode" class="mt-2 text-xs font-bold text-slate-500">已开启自动抬杠：点发送将随机记入一条（无需输入）。</p>
          <div class="mt-4 flex items-center gap-4 flex-wrap">
            <input
              v-model="quickReplyText"
              class="flex-1 min-w-[12rem] px-6 py-4 border-4 border-black rounded-3xl font-black bg-slate-50 focus:outline-none"
              placeholder="快速回喷..."
              type="text"
              :disabled="quickReplyLoading"
              @keyup.enter="quickReply"
            />
            <button
              class="bouncy-btn bg-black text-white px-6 py-4 rounded-3xl font-black disabled:opacity-50"
              type="button"
              :disabled="quickReplyLoading"
              @click="quickReply"
            >
              {{ quickReplyLoading ? '发送中…' : '发送' }}
            </button>
          </div>
        </div>
      </section>

      <section v-show="activeTab === 'settings'" class="space-y-8" id="settings">
        <div class="neo-panel p-10 bg-white">
          <h3 class="text-3xl humor-font font-black mb-8 flex items-center gap-4">⚙️ 设置（别乱动）</h3>
          <div class="space-y-6">
            <div class="neo-panel p-6 bg-white">
              <div class="flex items-center justify-between mb-4">
                <p class="font-black text-lg">资料编辑</p>
                <button class="bouncy-btn bg-black text-white px-4 py-2 rounded-xl font-black text-sm disabled:opacity-50" type="button" :disabled="savingProfile" @click="saveProfile">
                  保存
                </button>
              </div>
              <div v-if="saveProfileError" class="bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700 mb-4">
                {{ saveProfileError }}
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block font-black text-sm mb-2 ml-1">用户名</label>
                  <input v-model="editUsername" class="w-full px-4 py-3 border-4 border-black rounded-2xl font-bold bg-slate-50 focus:outline-none" type="text" />
                </div>
                <div>
                  <label class="block font-black text-sm mb-2 ml-1">邮箱</label>
                  <input v-model="editEmail" class="w-full px-4 py-3 border-4 border-black rounded-2xl font-bold bg-slate-50 focus:outline-none" type="email" />
                </div>
              </div>
              <div class="mt-4">
                <label class="block font-black text-sm mb-2 ml-1">头像（上传）</label>
                <div class="flex items-center gap-4">
                  <div class="w-16 h-16 border-4 border-black rounded-full overflow-hidden bg-slate-100">
                    <img class="w-full h-full object-cover" :src="editAvatarUrl || avatarUrlLarge" alt="avatar" />
                  </div>
                  <div class="flex-1">
                    <div class="flex flex-wrap gap-3">
                      <input ref="avatarFileEl" class="hidden" accept="image/*" type="file" @change="onAvatarFileChange" />
                      <button class="bouncy-btn bg-black text-white px-4 py-2 rounded-xl font-black text-sm disabled:opacity-50" type="button" :disabled="uploadingAvatar" @click="pickAvatar">
                        选择图片
                      </button>
                      <button
                        class="bouncy-btn bg-white border-4 border-black text-black px-4 py-2 rounded-xl font-black text-sm disabled:opacity-50"
                        type="button"
                        :disabled="uploadingAvatar || !pendingAvatarFile"
                        @click="uploadAvatar"
                      >
                        上传
                      </button>
                    </div>
                    <p v-if="avatarUploadError" class="mt-2 text-xs font-black text-red-600">{{ avatarUploadError }}</p>
                    <p v-else class="mt-2 text-xs font-bold text-slate-500">支持 png/jpg/webp/gif，最大 2MB</p>
                  </div>
                </div>
                <div class="mt-4">
                  <label class="block font-black text-sm mb-2 ml-1">头像链接（可选）</label>
                  <input v-model="editAvatarUrl" class="w-full px-4 py-3 border-4 border-black rounded-2xl font-bold bg-slate-50 focus:outline-none" type="text" />
                </div>
              </div>
              <div class="mt-4">
                <label class="block font-black text-sm mb-2 ml-1">个性签名</label>
                <textarea v-model="editBio" class="w-full px-4 py-3 border-4 border-black rounded-2xl font-bold bg-slate-50 focus:outline-none min-h-[110px]"></textarea>
              </div>
            </div>
            <div class="neo-panel p-6 bg-slate-50 flex items-center justify-between">
              <div>
                <p class="font-black text-lg">开启“自动抬杠”模式</p>
                <p class="text-xs font-bold text-slate-500">让系统替你在评论区发疯（危险）</p>
              </div>
              <input v-model="autoDebateMode" class="w-6 h-6 accent-pink-500" type="checkbox" @change="saveSettings" />
            </div>
            <div class="neo-panel p-6 bg-slate-50 flex items-center justify-between">
              <div>
                <p class="font-black text-lg">隐藏胜率</p>
                <p class="text-xs font-bold text-slate-500">输赢都当作没发生过</p>
              </div>
              <input v-model="hideWinRate" class="w-6 h-6 accent-blue-500" type="checkbox" @change="saveSettings" />
            </div>
            <div v-if="saveSettingsError" class="bg-red-100 border-4 border-black p-4 rounded-2xl font-black text-red-700">
              {{ saveSettingsError }}
            </div>
            <button class="bouncy-btn bg-red-500 text-white px-6 py-4 rounded-2xl font-black w-full" type="button" @click="logout">退出登录</button>
          </div>
        </div>
      </section>
    </main>

    <div v-if="publishPrompt.visible" class="fixed inset-0 z-[80] flex items-center justify-center p-6">
      <div class="absolute inset-0 bg-black/50" @click="closePublishPrompt"></div>
      <div class="relative neo-panel p-8 bg-white max-w-md w-full">
        <h4 class="text-3xl humor-font font-black mb-4">🪄 还没作品</h4>
        <p class="font-bold text-slate-700 mb-6">
          {{ publishPrompt.type === 'topic' ? '还没发过话题，要不要现在去发起一个？' : '还没发过文章，要不要现在去写一篇？' }}
        </p>
        <div class="flex items-center gap-4">
          <button class="bouncy-btn bg-black text-white px-5 py-3 rounded-2xl font-black flex-1" type="button" @click="confirmPublishPrompt">去发布</button>
          <button class="bouncy-btn bg-white border-4 border-black text-black px-5 py-3 rounded-2xl font-black flex-1" type="button" @click="closePublishPrompt">
            再看看
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch, watchEffect } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'

import { http } from '../api/http'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const allowedTabs = new Set(['overview', 'timeline', 'community', 'favorites', 'messages', 'settings'])
const activeTab = ref('overview')

const user = computed(() => auth.user)
const avatarUrlSmall = computed(() => user.value?.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(user.value?.username || 'guest')}`)
const avatarUrlLarge = computed(() => avatarUrlSmall.value)
const joinDateText = computed(() => {
  const v = user.value?.created_at
  if (!v) return '未知时间 加入'
  const d = new Date(v)
  if (Number.isNaN(d.getTime())) return '未知时间 加入'
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}年${m}月${day}日 加入`
})

const stats = ref(null)
const statAnimated = ref({
  topics_created: 0,
  debate_posts: 0,
  blog_posts: 0,
  followers: 0,
  likes_total: 0
})
const badges = ref([])
const heatmap = ref({ days: [] })
const activityItems = ref([])
/** 从码字心电图点选某一天后，在时间线里按「本地日历日」筛选（YYYY-MM-DD） */
const activityFilterDate = ref('')

const activityLocalDayKey = (v) => {
  const d = new Date(v)
  if (Number.isNaN(d.getTime())) return ''
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

const displayActivityItems = computed(() => {
  const day = activityFilterDate.value
  if (!day) return activityItems.value
  return activityItems.value.filter((it) => activityLocalDayKey(it.created_at) === day)
})

const activityFilterDateLabel = computed(() => {
  const s = activityFilterDate.value
  if (!s) return ''
  const p = s.split('-')
  if (p.length !== 3) return s
  return `${p[0]}年${Number(p[1])}月${Number(p[2])}日`
})

const followersItems = ref([])
const followingItems = ref([])
const favoriteItems = ref([])
const notificationItems = ref([])
const myTopics = ref([])
const myBlogPosts = ref([])
const myDebatePosts = ref([])
const publishPrompt = ref({ visible: false, type: '' })

const editUsername = ref('')
const editEmail = ref('')
const editAvatarUrl = ref('')
const editBio = ref('')
const autoDebateMode = ref(false)
const hideWinRate = ref(false)
const savingProfile = ref(false)
const saveProfileError = ref('')

const avatarFileEl = ref(null)
const pendingAvatarFile = ref(null)
const uploadingAvatar = ref(false)
const avatarUploadError = ref('')
const saveSettingsError = ref('')

const unreadCount = computed(() => notificationItems.value.filter((n) => !n.is_read).length)
const quickReplyText = ref('')

const activityHasMore = ref(false)
const activityBeforeId = ref(null)
const loadingMoreActivity = ref(false)

const favoritesHasMore = ref(false)
const favoritesBeforeId = ref(null)
const loadingMoreFavorites = ref(false)

const notificationsHasMore = ref(false)
const notificationsBeforeId = ref(null)
const loadingMoreNotifications = ref(false)

const badgeSrc = (id) => `/badges/${id || 'badge-star'}.svg`

const animateInt = (from, to, ms = 700) => {
  const a = Number(from || 0)
  const b = Number(to || 0)
  if (!Number.isFinite(a) || !Number.isFinite(b)) return b
  if (ms <= 0) return Math.round(b)
  const start = performance.now()
  return new Promise((resolve) => {
    const tick = (now) => {
      const t = Math.min(1, (now - start) / ms)
      const eased = 1 - Math.pow(1 - t, 3)
      resolve(Math.round(a + (b - a) * eased))
      if (t < 1) requestAnimationFrame(tick)
    }
    requestAnimationFrame(tick)
  })
}

const animateStats = async (next) => {
  if (!next) return
  const keys = ['topics_created', 'debate_posts', 'blog_posts', 'followers', 'likes_total']
  for (const k of keys) {
    const from = statAnimated.value[k] || 0
    const to = Number(next?.[k] || 0)
    statAnimated.value[k] = await animateInt(from, to, 720)
  }
}

const countToLevel = (count) => {
  if (!count) return 0
  if (count === 1) return 1
  if (count <= 3) return 2
  if (count <= 6) return 3
  return 4
}

const heatmapCells = computed(() => {
  const days = heatmap.value?.days || []
  return days.map((d) => ({ ...d, level: countToLevel(d.count) }))
})

const heatmapTotal = computed(() => (heatmap.value?.days || []).reduce((sum, d) => sum + (d.count || 0), 0))

const switchTab = (tabId) => {
  if (!allowedTabs.has(tabId)) return
  activeTab.value = tabId
  router.replace({ hash: `#${tabId}` })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const heatmapCellTitle = (cell) => {
  const c = Number(cell?.count || 0)
  const d = cell?.date || ''
  return `${d}：${c} 次 · 点击查看该日时间线`
}

const onHeatmapCellClick = (cell) => {
  if (!cell?.date) return
  activityFilterDate.value = String(cell.date)
  switchTab('timeline')
}

const clearActivityDayFilter = () => {
  activityFilterDate.value = ''
}

const overviewStatNum = (key) => {
  const n = Number(stats.value?.[key] ?? 0)
  return Number.isFinite(n) ? n : 0
}

/** 统计加载完成后，发起话题 / 观点 / 博客 三块可点：无作品去发布，有作品去对应列表 */
const overviewStatClickable = (key) => {
  if (!stats.value) return false
  return key === 'topics_created' || key === 'debate_posts' || key === 'blog_posts'
}

const overviewStatTitle = (key) => {
  if (!stats.value) return ''
  if (key === 'topics_created') {
    return overviewStatNum(key) === 0 ? '暂无话题，点此去发起' : '查看个人中心 · 我的话题列表'
  }
  if (key === 'debate_posts') {
    return overviewStatNum(key) === 0 ? '暂无观点，点此去话题池' : '查看个人中心 · 我的观点列表'
  }
  if (key === 'blog_posts') {
    return overviewStatNum(key) === 0 ? '暂无文章，点此去写博客' : '前往胡说博客 · 文章列表'
  }
  return ''
}

const goProfileOverviewAnchor = (hash) => {
  activeTab.value = 'overview'
  router.push({ path: '/profile', hash })
}

const onOverviewStatClick = (kind) => {
  if (!stats.value) return
  if (kind === 'topics_created') {
    if (overviewStatNum('topics_created') === 0) {
      router.push({ path: '/debate-list', query: { create: '1' } })
    } else {
      goProfileOverviewAnchor('#profile-my-topics')
    }
    return
  }
  if (kind === 'debate_posts') {
    if (overviewStatNum('debate_posts') === 0) {
      router.push({ path: '/debate-list' })
    } else {
      goProfileOverviewAnchor('#profile-my-debates')
    }
    return
  }
  if (kind === 'blog_posts') {
    if (overviewStatNum('blog_posts') === 0) {
      router.push({ path: '/blog', query: { create: '1' } })
    } else {
      router.push({ path: '/blog' })
    }
  }
}

const tabBtnClass = (tabId, hoverClass) => {
  const base = ['nav-btn', 'w-12', 'h-12', 'md:w-16', 'md:h-16', 'flex', 'items-center', 'justify-center', 'border-4', 'border-black', 'rounded-2xl', 'transition-all', hoverClass]
  if (activeTab.value === tabId) base.unshift('tab-active')
  return base.join(' ')
}

const quickReplyLoading = ref(false)
const quickReplyHint = ref('')

const quickReply = async () => {
  quickReplyHint.value = ''
  await ensureUser()
  if (!user.value?.id) return
  quickReplyLoading.value = true
  try {
    if (autoDebateMode.value) {
      const r = await http.post('users/me/quick-reply/', { auto: true })
      quickReplyHint.value = r?.text ? `已记录：${r.text}` : '已记录一条自动抬杠'
      quickReplyText.value = ''
    } else {
      const t = quickReplyText.value.trim()
      if (!t) {
        quickReplyHint.value = '先输入你想回喷的话'
        return
      }
      await http.post('users/me/quick-reply/', { text: t })
      quickReplyText.value = ''
      quickReplyHint.value = '回喷已记入活动时间线'
    }
    await loadTimeline().catch(() => {})
    if (activeTab.value === 'overview') await loadOverview().catch(() => {})
  } catch (e) {
    quickReplyHint.value = e?.message || '发送失败'
  } finally {
    quickReplyLoading.value = false
  }
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

const activityLabel = (actionType) => {
  const map = {
    create_topic: '发起话题',
    post_debate: '发表观点',
    publish_blog: '发布博客',
    follow: '关注',
    quick_reply: '快速回喷'
  }
  return map[actionType] || actionType
}

const activityDotClass = (actionType) => {
  const map = {
    create_topic: 'bg-pink-500',
    post_debate: 'bg-blue-500',
    publish_blog: 'bg-yellow-400',
    follow: 'bg-green-400',
    quick_reply: 'bg-orange-400'
  }
  return map[actionType] || 'bg-slate-400'
}

const activityTagClass = (actionType) => {
  const map = {
    create_topic: 'bg-pink-500',
    post_debate: 'bg-blue-500',
    publish_blog: 'bg-black',
    follow: 'bg-green-500',
    quick_reply: 'bg-orange-500'
  }
  return map[actionType] || 'bg-slate-400'
}

const activityTitle = (item) => {
  const data = item?.data || {}
  if (item.action_type === 'create_topic' && data.title) return data.title
  if (item.action_type === 'publish_blog' && data.title) return data.title
  if (item.action_type === 'post_debate' && data.content) return data.content
  if (item.action_type === 'follow' && data.followee) return `关注了 ${data.followee}`
  if (item.action_type === 'quick_reply' && data.text) return data.text
  return `${activityLabel(item.action_type)}`
}

const activityDesc = (item) => {
  const data = item?.data || {}
  if (data.content && item.action_type !== 'post_debate') return data.content
  return ''
}

const favoriteTypeText = (t) => {
  const map = { topic: '话题', blog_post: '文章', debate_post: '观点' }
  return map[t] || t
}

const favoriteTitle = (f) => {
  const t = f.target || {}
  return t.title || t.content || `#${f.target_id}`
}

const openPublishPrompt = (type) => {
  publishPrompt.value = { visible: true, type }
}

const closePublishPrompt = () => {
  publishPrompt.value = { visible: false, type: '' }
}

const confirmPublishPrompt = () => {
  const type = publishPrompt.value.type
  closePublishPrompt()
  if (type === 'topic') {
    router.push({ path: '/debate-list', query: { create: '1' } })
    return
  }
  if (type === 'blog') {
    router.push({ path: '/blog', query: { create: '1' } })
  }
}

const goDebateList = () => {
  router.push('/debate-list')
}

const favoriteTo = (f) => {
  if (f.target_type === 'blog_post') return { path: '/blog-detail', query: { id: String(f.target_id), slug: f.target?.slug || '' } }
  if (f.target_type === 'topic') return { path: '/debate-detail', query: { id: String(f.target_id) } }
  if (f.target_type === 'debate_post') {
    const topicId = f.target?.topic_id
    if (topicId) return { path: '/debate-detail', query: { id: String(topicId) } }
    return '/debate-list'
  }
  return '/profile#favorites'
}

const asObject = (v) => {
  if (!v) return {}
  if (typeof v === 'object') return v
  if (typeof v !== 'string') return {}
  try {
    const o = JSON.parse(v)
    return o && typeof o === 'object' ? o : {}
  } catch {
    return {}
  }
}

const notificationTitle = (n) => {
  const data = asObject(n.data)
  if (data.actor) return data.actor
  return n.type
}

const notificationBody = (n) => {
  const data = asObject(n.data)
  if (data.content && data.target) return `${data.content}：${data.target}`
  if (data.content) return data.content
  return ''
}

const openActivity = (item) => {
  const t = item?.target_type
  const id = item?.target_id
  if (!t || !id) return
  if (t === 'topic') {
    router.push({ path: '/debate-detail', query: { id: String(id) } })
    return
  }
  if (t === 'blog_post') {
    router.push({ path: '/blog-detail', query: { id: String(id) } })
    return
  }
  if (t === 'debate_post') {
    const data = asObject(item?.data)
    const topicId = data.topic_id
    if (topicId) {
      router.push({ path: '/debate-detail', query: { id: String(topicId) } })
      return
    }
    router.push('/debate-list')
  }
}

const openNotification = async (n) => {
  if (!n) return
  const data = asObject(n.data)
  const t = data.target_type
  const id = data.target_id
  if (!n.is_read) {
    await markRead(n.id).catch(() => {})
  }
  if (!t || !id) return
  if (t === 'topic') {
    router.push({ path: '/debate-detail', query: { id: String(id) } })
    return
  }
  if (t === 'blog_post') {
    router.push({ path: '/blog-detail', query: { id: String(id) } })
    return
  }
  if (t === 'debate_post') {
    const topicId = data.topic_id
    if (topicId) {
      router.push({ path: '/debate-detail', query: { id: String(topicId) } })
      return
    }
    router.push('/debate-list')
  }
}

const ensureUser = async () => {
  if (!auth.user && auth.isAuthed) {
    await auth.fetchProfile()
  }
}

const syncEditFromUser = () => {
  editUsername.value = user.value?.username || ''
  editEmail.value = user.value?.email || ''
  editAvatarUrl.value = user.value?.avatar_url || ''
  editBio.value = user.value?.bio || ''
  autoDebateMode.value = !!user.value?.auto_debate_mode
  hideWinRate.value = !!user.value?.hide_win_rate
  pendingAvatarFile.value = null
  avatarUploadError.value = ''
}

const saveSettings = async () => {
  await ensureUser()
  if (!user.value?.id) return
  saveSettingsError.value = ''
  try {
    await http.patch('auth/profile/', {
      auto_debate_mode: autoDebateMode.value,
      hide_win_rate: hideWinRate.value
    })
    await auth.fetchProfile().catch(() => {})
    syncEditFromUser()
  } catch (e) {
    saveSettingsError.value = e?.message || '保存失败'
  }
}

const pickAvatar = () => {
  avatarUploadError.value = ''
  avatarFileEl.value?.click?.()
}

const onAvatarFileChange = (e) => {
  const f = e?.target?.files?.[0]
  pendingAvatarFile.value = f || null
}

const uploadAvatar = async () => {
  if (!pendingAvatarFile.value) return
  avatarUploadError.value = ''
  uploadingAvatar.value = true
  try {
    const fd = new FormData()
    fd.append('file', pendingAvatarFile.value)
    const r = await http.post('auth/avatar/', fd)
    editAvatarUrl.value = r?.avatar_url || editAvatarUrl.value
    await auth.fetchProfile()
    syncEditFromUser()
  } catch (e) {
    avatarUploadError.value = e?.message || '上传失败'
  } finally {
    uploadingAvatar.value = false
    if (avatarFileEl.value) avatarFileEl.value.value = ''
    pendingAvatarFile.value = null
  }
}

const saveProfile = async () => {
  saveProfileError.value = ''
  savingProfile.value = true
  try {
    await http.patch('auth/profile/', {
      username: editUsername.value,
      email: editEmail.value,
      avatar_url: editAvatarUrl.value,
      bio: editBio.value,
      auto_debate_mode: autoDebateMode.value,
      hide_win_rate: hideWinRate.value
    })
    await auth.fetchProfile()
    syncEditFromUser()
  } catch (e) {
    saveProfileError.value = e?.message || '保存失败'
  } finally {
    savingProfile.value = false
  }
}

const loadMyContent = async () => {
  await ensureUser()
  if (!user.value?.id) return
  const r = await http.get(`users/${user.value.id}/content/`, { params: { limit: 6 } })
  myTopics.value = r?.topics || []
  myBlogPosts.value = r?.blog_posts || []
  myDebatePosts.value = r?.debate_posts || []
}

const loadOverview = async () => {
  await ensureUser()
  if (!user.value?.id) return
  const [s, b, h] = await Promise.all([
    http.get(`users/${user.value.id}/stats/`),
    http.get(`users/${user.value.id}/badges/`),
    http.get(`users/${user.value.id}/heatmap/`)
  ])
  stats.value = s
  badges.value = (b?.items || []).slice(0, 12)
  heatmap.value = h
  await loadMyContent().catch(() => {})
}

const loadTimeline = async () => {
  await ensureUser()
  if (!user.value?.id) return
  const r = await http.get(`users/${user.value.id}/activity/`, { params: { limit: 30 } })
  activityItems.value = r?.items || []
  activityHasMore.value = !!(r?.has_more ?? r?.hasMore)
  activityBeforeId.value = (r?.next_before_id ?? r?.nextBeforeId) || (activityItems.value.length ? activityItems.value[activityItems.value.length - 1].id : null)
}

const loadMoreTimeline = async () => {
  if (loadingMoreActivity.value) return
  if (!activityHasMore.value || !activityBeforeId.value) return
  loadingMoreActivity.value = true
  try {
    const r = await http.get(`users/${user.value.id}/activity/`, { params: { limit: 30, before_id: activityBeforeId.value } })
    const next = r?.items || []
    activityItems.value = activityItems.value.concat(next)
    activityHasMore.value = !!(r?.has_more ?? r?.hasMore)
    activityBeforeId.value = (r?.next_before_id ?? r?.nextBeforeId) || (next.length ? next[next.length - 1].id : activityBeforeId.value)
  } finally {
    loadingMoreActivity.value = false
  }
}

const loadCommunity = async () => {
  await ensureUser()
  if (!user.value?.id) return
  const [followers, following] = await Promise.all([
    http.get(`users/${user.value.id}/followers/`),
    http.get(`users/${user.value.id}/following/`)
  ])
  followersItems.value = followers?.items || []
  followingItems.value = following?.items || []
}

const loadFavorites = async () => {
  await ensureUser()
  const r = await http.get('favorites/', { params: { limit: 20 } })
  favoriteItems.value = r?.items || []
  favoritesHasMore.value = !!(r?.has_more ?? r?.hasMore)
  favoritesBeforeId.value = (r?.next_before_id ?? r?.nextBeforeId) || (favoriteItems.value.length ? favoriteItems.value[favoriteItems.value.length - 1].id : null)
}

const loadMoreFavorites = async () => {
  if (loadingMoreFavorites.value) return
  if (!favoritesHasMore.value || !favoritesBeforeId.value) return
  loadingMoreFavorites.value = true
  try {
    const r = await http.get('favorites/', { params: { limit: 20, before_id: favoritesBeforeId.value } })
    const next = r?.items || []
    favoriteItems.value = favoriteItems.value.concat(next)
    favoritesHasMore.value = !!(r?.has_more ?? r?.hasMore)
    favoritesBeforeId.value = (r?.next_before_id ?? r?.nextBeforeId) || (next.length ? next[next.length - 1].id : favoritesBeforeId.value)
  } finally {
    loadingMoreFavorites.value = false
  }
}

const removeFavorite = async (f) => {
  if (!f?.target_type || !f?.target_id) return
  await http.delete('favorites/', { params: { target_type: f.target_type, target_id: f.target_id } })
  favoriteItems.value = favoriteItems.value.filter((x) => x.id !== f.id)
}

const loadMessages = async () => {
  await ensureUser()
  const r = await http.get('notifications/', { params: { limit: 20 } })
  notificationItems.value = r?.items || []
  notificationsHasMore.value = !!(r?.has_more ?? r?.hasMore)
  notificationsBeforeId.value = (r?.next_before_id ?? r?.nextBeforeId) || (notificationItems.value.length ? notificationItems.value[notificationItems.value.length - 1].id : null)
}

const loadMoreNotifications = async () => {
  if (loadingMoreNotifications.value) return
  if (!notificationsHasMore.value || !notificationsBeforeId.value) return
  loadingMoreNotifications.value = true
  try {
    const r = await http.get('notifications/', { params: { limit: 20, before_id: notificationsBeforeId.value } })
    const next = r?.items || []
    notificationItems.value = notificationItems.value.concat(next)
    notificationsHasMore.value = !!(r?.has_more ?? r?.hasMore)
    notificationsBeforeId.value = (r?.next_before_id ?? r?.nextBeforeId) || (next.length ? next[next.length - 1].id : notificationsBeforeId.value)
  } finally {
    loadingMoreNotifications.value = false
  }
}

const refreshAll = async () => {
  await Promise.all([loadOverview(), loadTimeline(), loadCommunity(), loadFavorites(), loadMessages()].map((p) => p.catch(() => {})))
}

const followingIdSet = computed(() => new Set(followingItems.value.map((u) => u.id)))

const follow = async (id) => {
  await http.post(`users/${id}/follow/`, {})
  await loadCommunity()
}

const unfollow = async (id) => {
  await http.delete(`users/${id}/follow/`)
  await loadCommunity()
}

const markRead = async (id) => {
  try {
    await http.patch(`notifications/${id}/read/`, {})
  } catch {
    await loadMessages().catch(() => {})
    return
  }
  const i = notificationItems.value.findIndex((x) => x.id === id)
  if (i >= 0) notificationItems.value[i] = { ...notificationItems.value[i], is_read: true }
}

const markAllRead = async () => {
  await http.post('notifications/read-all/', {})
  await loadMessages()
}

const logout = async () => {
  await auth.logout()
  router.replace('/')
}

const loadActiveTab = async (tabId) => {
  if (tabId === 'overview') return loadOverview()
  if (tabId === 'timeline') return loadTimeline()
  if (tabId === 'community') return loadCommunity()
  if (tabId === 'favorites') return loadFavorites()
  if (tabId === 'messages') return loadMessages()
}

watchEffect(() => {
  const hash = (route.hash || '').replace('#', '')
  if (allowedTabs.has(hash)) activeTab.value = hash
  loadActiveTab(activeTab.value).catch(() => {})
})

onMounted(() => {
  loadActiveTab(activeTab.value).catch(() => {})
  syncEditFromUser()
})

watch(
  () => stats.value,
  (s) => {
    animateStats(s).catch(() => {})
  }
)
</script>

<style>
:root {
  --primary: #ff477e;
  --secondary: #ffbe0b;
  --accent: #3a86ff;
  --bg-light: #fdf0d5;
  --mint: #06d6a0;
  --purple: #8338ec;
  --black: #000000;
}

body {
  background-color: var(--bg-light);
  color: var(--black);
  overflow-x: hidden;
}

.humor-font {
  font-family: 'ZCOOL KuaiLe', cursive;
}

.neo-panel {
  background: white;
  border: 4px solid black;
  box-shadow: 8px 8px 0px black;
  border-radius: 24px;
  transition: all 0.2s;
}

.neo-panel:hover {
  transform: translate(-2px, -2px);
  box-shadow: 10px 10px 0px black;
}

.bouncy-btn {
  transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 3px solid black;
  box-shadow: 4px 4px 0px black;
}

.bouncy-btn:hover {
  transform: scale(1.05) rotate(-1deg);
  box-shadow: 6px 6px 0px black;
}

.bouncy-btn:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0px black;
}

.tab-active {
  background-color: var(--secondary) !important;
  transform: scale(1.1) rotate(-2deg);
  z-index: 10;
}

.heatmap-grid {
  display: grid;
  grid-template-columns: repeat(20, 1fr);
  gap: 4px;
}

.heatmap-cell {
  aspect-ratio: 1;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.level-0 {
  background: #eee;
}

.level-1 {
  background: #d1fae5;
}

.level-2 {
  background: #6ee7b7;
}

.level-3 {
  background: #10b981;
}

.level-4 {
  background: #047857;
}

.timeline-line {
  position: absolute;
  left: 20px;
  top: 0;
  bottom: 0;
  width: 4px;
  background: black;
  z-index: 0;
}

.badge-dot {
  position: absolute;
  top: -5px;
  right: -5px;
  background: var(--primary);
  color: white;
  border: 2px solid black;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.abstract-shape {
  clip-path: polygon(10% 0, 100% 0%, 90% 100%, 0% 100%);
}
</style>
