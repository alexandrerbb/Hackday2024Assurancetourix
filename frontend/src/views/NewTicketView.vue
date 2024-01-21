<script setup lang="ts">
import { ref } from 'vue'
import { NPageHeader, NButton, NIcon } from 'naive-ui'
import { Email } from '@vicons/carbon'

import router from '@/router'
import { useApi } from '@/composables/useApi'
import CustomerResponse from '@/components/CustomerResponse.vue'

const { fetch } = useApi()

const { data: defaultOptions } = fetch('start_options').json()

const ticketUpdate = ref({ option: undefined, message: undefined })

const { isFetching, execute } = fetch('new', {
  immediate: false,
  afterFetch(ctx: { data: { id: string } }) {
    const { data } = ctx
    if (!data) {
      return ctx
    }
    router.push({ name: 'ticket', params: { id: data.id } })
    return ctx
  }
})
  .post(ticketUpdate)
  .json()
</script>

<template>
  <n-page-header
    title="Envoyer un message au service client."
    @back.prevent="router.push({ name: 'home' })"
  />
  <customer-response :options="defaultOptions" v-model="ticketUpdate" v-if="defaultOptions" />
  <n-button @click="execute()" :loading="isFetching">
    <template #icon>
      <n-icon>
        <email />
      </n-icon>
    </template>
    Envoyer un nouveau message
  </n-button>
</template>
