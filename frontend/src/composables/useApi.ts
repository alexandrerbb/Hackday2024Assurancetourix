import { createFetch, useLocalStorage } from '@vueuse/core'
import { useMessage } from 'naive-ui'
import router from '@/router'

const useApiUrl = (apiPath: string) => `${import.meta.env.VITE_API_HOST}/apis/${apiPath}`
const baseUrl = useApiUrl('tickets/v1/')

interface AutenticationResponse {
  accessToken: string
  tokenType: string
  user: {
    id: string
    username: string
  }
}

export function useApi() {
  const token = useLocalStorage<string>('token', '')
  const message = useMessage()

  const fetch = createFetch({
    baseUrl,
    options: {
      async beforeFetch({ options }: { options: RequestInit }) {
        options.headers = { ...options.headers, ...{ Authorization: 'Bearer ' + token.value } }
        return { options }
      },
      onFetchError(ctx) {
        if (ctx.response?.status == 401) {
          router.push({ name: 'login' })
        } else {
          message.error('Une erreur a été encontrée lors du chargement des données.')
        }
        return ctx
      }
    }
  })

  const useAuthenticate = createFetch({
    baseUrl: useApiUrl('auth/v1/'),
    options: {
      immediate: false,
      afterFetch(ctx: { data: AutenticationResponse }) {
        const { data } = ctx
        if (!data) {
          return ctx
        }
        token.value = data.accessToken
        router.push({ name: 'home' })
        message.success(`Connecté en tant que ${data.user.username}.`)
        return ctx
      },
      onFetchError(ctx) {
        message.error('Identifiants incorrects.')
        return ctx
      }
    }
  })

  const authenticate = (credentials: { username: string; password: string }) =>
    useAuthenticate<AutenticationResponse>('login').post(credentials).json()

  return { authenticate, fetch }
}
