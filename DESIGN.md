# DESIGN

## 目标
- 视觉风格：粗边框 + 硬阴影 + 强对比 + 俏皮但可读
- 代码落地：优先 Tailwind 组合类，少写自定义 CSS；需要新增时集中在 assets
- 一致性：同类组件同一交互与状态呈现（loading/empty/error/disabled）

## 布局与间距
- 页面容器：优先 max-w-7xl + mx-auto + px-6
- 区块间距：优先 gap-6 / gap-8；避免同页出现太多不同间距尺度
- 卡片内边距：优先 p-6 / p-8；小卡可用 p-4

## 排版
- 标题：text-2xl~4xl + font-black + tracking-tight
- 副标题/说明：text-sm~base + font-bold/semibold + 提高对比度
- 正文：leading-6~7；长文避免过浅的灰色

## 边框与阴影
- 边框：多用 border-4 border-black
- 阴影：优先“硬阴影”形态，例如 shadow-[6px_6px_0px_black]
- Active：按下态用 active:translate-y-1 + active:shadow-none

## 组件状态（最低要求）
- Loading：禁用重复提交；必要时骨架/占位
- Empty：明确空态 + 可继续操作入口
- Error：就地错误信息 + 重试/返回入口
- Auth：未登录/无权限/仅本人可见需明确提示

## Icon
- 统一使用 Iconify（图标来源尽量同一套系，例如 mdi）
- 代码层面统一使用 Vue 组件 `<Icon />`（全局注册）
- 图标按钮必须有 aria-label；纯装饰图标使用 aria-hidden
- 尺寸建议：18/20/24（行内），48/80/120（强调），100~300（装饰慎用）

## Motion
- 页面转场：使用 `Transition name="page"`（见 frontend/src/assets/motion.css）
- 滚动出现：使用 `v-reveal`（支持延迟）
- 漂浮装饰：float-slow / float-fast
- 必须尊重减少动效偏好：reduce 模式下不应闪烁或影响可用性

## 文案与语气
- 中文优先，短句、强动词
- 允许俏皮，但错误/权限提示要清晰可执行
- 避免过度堆 emoji；图标与 emoji 二选一时优先图标

