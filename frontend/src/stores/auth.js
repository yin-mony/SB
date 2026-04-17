import { defineStore } from 'pinia'

import { http } from '../api/http'

const readStored = (key) => sessionStorage.getItem(key) || localStorage.getItem(key) || ''

const clearAllAuthKeys = () => {
  for (const k of ['auth_user', 'access_token', 'refresh_token']) {
    sessionStorage.removeItem(k)
    localStorage.removeItem(k)
  }
}

const persistUserToActiveStorage = (user) => {
  const s = JSON.stringify(user)
  if (sessionStorage.getItem('access_token')) sessionStorage.setItem('auth_user', s)
  else localStorage.setItem('auth_user', s)
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(readStored('auth_user') || 'null'),
    accessToken: readStored('access_token'),
    refreshToken: readStored('refresh_token')
  }),
  getters: {
    isAuthed: (state) => Boolean(state.accessToken)
  },
  actions: {
    setSession({ user, access, refresh }, { rememberMe = true } = {}) {
      const primary = rememberMe ? localStorage : sessionStorage
      const secondary = rememberMe ? sessionStorage : localStorage
      for (const k of ['auth_user', 'access_token', 'refresh_token']) {
        secondary.removeItem(k)
      }
      primary.setItem('auth_user', JSON.stringify(user))
      primary.setItem('access_token', access)
      primary.setItem('refresh_token', refresh)
      this.user = user
      this.accessToken = access
      this.refreshToken = refresh
    },
    clearSession() {
      this.user = null
      this.accessToken = ''
      this.refreshToken = ''
      clearAllAuthKeys()
    },
    async login({ account, password, rememberMe = true }) {
      const data = await http.post('auth/login/', { account, password })
      this.setSession(
        {
          user: data.user,
          access: data.token.access,
          refresh: data.token.refresh
        },
        { rememberMe }
      )
      return data.user
    },
    async register({ username, password, captcha_id, captcha }, { rememberMe = true } = {}) {
      const data = await http.post('auth/register/', { username, password, captcha_id, captcha })
      this.setSession(
        {
          user: data.user,
          access: data.token.access,
          refresh: data.token.refresh
        },
        { rememberMe }
      )
      return data.user
    },
    async fetchProfile() {
      const user = await http.get('auth/profile/')
      this.user = user
      persistUserToActiveStorage(user)
      return user
    },
    async logout() {
      try {
        const refresh =
          this.refreshToken || readStored('refresh_token')
        if (refresh) {
          await http.post('auth/logout/', { refresh })
        }
      } catch (e) {
      } finally {
        this.clearSession()
      }
    }
  }
})
