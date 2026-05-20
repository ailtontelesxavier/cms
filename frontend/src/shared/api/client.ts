import axios, { type AxiosError, type AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

export type ApiError = AxiosError<{ detail?: string }>

export function isApiError(error: unknown): error is ApiError {
  return axios.isAxiosError(error)
}

export function getApiErrorMessage(error: unknown): string {
  if (isApiError(error)) {
    return error.response?.data?.detail || error.message || 'Erro de conexão'
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'Erro desconhecido'
}

const client: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

let tokenInterceptorId: number | null = null

export function setAuthToken(token: string | null): void {
  if (tokenInterceptorId !== null) {
    client.interceptors.request.eject(tokenInterceptorId)
    tokenInterceptorId = null
  }

  if (token) {
    tokenInterceptorId = client.interceptors.request.use((config) => {
      config.headers.Authorization = `Bearer ${token}`
      return config
    })
  }
}

export function createApiClient(): AxiosInstance {
  return client
}

export default client
