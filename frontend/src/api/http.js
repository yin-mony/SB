import axios from 'axios'

const getAccessToken = () => sessionStorage.getItem('access_token') || localStorage.getItem('access_token') || ''

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1/',
  timeout: 15000
})

http.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (resp) => {
    const data = resp?.data
    if (data && typeof data === 'object' && 'code' in data && 'msg' in data && 'data' in data) {
      if (data.code !== 200) {
        const err = new Error(data.msg || '请求失败')
        err.response = resp
        throw err
      }
      return data.data
    }
    return resp
  },
  (err) => {
    if (!err?.response) {
      const e = new Error('无法连接服务器，请确认后端已启动（http://127.0.0.1:8000）')
      e.cause = err
      return Promise.reject(e)
    }
    const status = err?.response?.status
    if (status === 401) {
      sessionStorage.removeItem('access_token')
      sessionStorage.removeItem('refresh_token')
      sessionStorage.removeItem('auth_user')
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('auth_user')
      const path = window.location.pathname + window.location.search + window.location.hash
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = `/login?redirect=${encodeURIComponent(path)}`
        return
      }
    }
    const body = err?.response?.data
    let message = ''
    if (body && typeof body === 'object') {
      const nested = body.data
      if (nested && typeof nested === 'object') {
        for (const key of Object.keys(nested)) {
          const v = nested[key]
          if (Array.isArray(v) && v.length) {
            message = String(v[0])
            break
          }
          if (typeof v === 'string' && v) {
            message = v
            break
          }
        }
      }
      if (!message && typeof body.msg === 'string' && body.msg) {
        message = body.msg
      } else if (!message && typeof body.detail === 'string' && body.detail) {
        message = body.detail
      } else if (!message && Array.isArray(body.detail) && body.detail.length) {
        message = String(body.detail[0])
      } else if (!message) {
        for (const key of Object.keys(body)) {
          if (key === 'code' || key === 'data' || key === 'msg') continue
          const v = body[key]
          if (Array.isArray(v) && v.length) {
            message = String(v[0])
            break
          }
          if (typeof v === 'string' && v) {
            message = v
            break
          }
        }
      }
    }
    if (message) {
      const wrapped = new Error(message)
      wrapped.response = err.response
      return Promise.reject(wrapped)
    }
    return Promise.reject(err)
  }
)
