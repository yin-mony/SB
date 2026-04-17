import { createApp } from 'vue'
import { Icon } from '@iconify/vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import './assets/legacy-shared.css'
import './assets/motion.css'

const app = createApp(App)
app.component('Icon', Icon)

const installRevealDirective = (appInstance) => {
  if (typeof window === 'undefined') return
  if (!('IntersectionObserver' in window)) {
    appInstance.directive('reveal', {
      mounted(el) {
        el.classList.add('reveal', 'is-visible')
      }
    })
    return
  }

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue
        entry.target.classList.add('is-visible')
        observer.unobserve(entry.target)
      }
    },
    { threshold: 0.12 }
  )

  appInstance.directive('reveal', {
    mounted(el, binding) {
      el.classList.add('reveal')
      const delay = Number(binding?.value || 0)
      if (Number.isFinite(delay) && delay > 0) el.style.transitionDelay = `${delay}ms`
      observer.observe(el)
    },
    unmounted(el) {
      observer.unobserve(el)
    }
  })
}

installRevealDirective(app)

app.use(createPinia()).use(router).mount('#app')
