<script setup lang="ts">
import { ref } from 'vue'
import { NInput, NCard, NButton, NForm, NFormItem } from 'naive-ui'

import { useApi } from '@/composables/useApi'

const { authenticate } = useApi()

const userCredentials = ref<{ username: string; password: string }>({ username: '', password: '' })
const { execute, isFetching } = authenticate(userCredentials.value)
</script>

<template>
  <n-card title="Connexion" size="large">
    <n-form :model="userCredentials">
      <n-form-item label="Nom d'utilisateur" path="username">
        <n-input
          v-model:value="userCredentials.username"
          type="text"
          placeholder="Nom d'utilisateur"
          :input-props="{ autocomplete: 'username' }"
        />
      </n-form-item>
      <n-form-item label="Mot de passe" path="password">
        <n-input
          v-model:value="userCredentials.password"
          type="password"
          placeholder="Mot de passe"
          @keyup.enter="execute()"
          :input-props="{ autocomplete: 'current-password' }"
        />
      </n-form-item>
      <n-button @click="execute()" :loading="isFetching">Connexion</n-button>
    </n-form>
  </n-card>
</template>

<style scoped>
.n-card {
  width: 100vw;
  max-width: 40rem;
}
</style>
