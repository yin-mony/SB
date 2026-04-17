import { createRouter, createWebHistory } from 'vue-router'
import IndexView from '../views/IndexView.vue'
import DebateListView from '../views/DebateListView.vue'
import DebateDetailView from '../views/DebateDetailView.vue'
import BlogListView from '../views/BlogListView.vue'
import BlogDetailView from '../views/BlogDetailView.vue'
import FaqView from '../views/FaqView.vue'
import AboutView from '../views/AboutView.vue'
import ResourcesView from '../views/ResourcesView.vue'
import RulesView from '../views/RulesView.vue'
import TournamentView from '../views/TournamentView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ForgotPasswordView from '../views/ForgotPasswordView.vue'
import ResetPasswordView from '../views/ResetPasswordView.vue'
import ProfileView from '../views/ProfileView.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', name: 'home', component: IndexView },
  { path: '/debate-list', name: 'debate-list', component: DebateListView },
  { path: '/debate-detail', name: 'debate-detail', component: DebateDetailView },
  { path: '/blog', name: 'blog', component: BlogListView },
  { path: '/blog-detail', name: 'blog-detail', component: BlogDetailView },
  { path: '/about', name: 'about', component: AboutView },
  { path: '/faq', name: 'faq', component: FaqView },
  { path: '/resources', name: 'resources', component: ResourcesView },
  { path: '/rules', name: 'rules', component: RulesView },
  { path: '/tournament', name: 'tournament', component: TournamentView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/forgot-password', name: 'forgot-password', component: ForgotPasswordView },
  { path: '/reset-password', name: 'reset-password', component: ResetPasswordView },
  { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, _from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth', top: 96 }
    }
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta?.requiresAuth && !auth.isAuthed) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
})

router.afterEach((to) => {
  if (to.path !== '/login' && to.path !== '/register' && to.path !== '/forgot-password' && to.path !== '/reset-password') {
    sessionStorage.setItem('last_path', to.fullPath)
  }
})

export default router
