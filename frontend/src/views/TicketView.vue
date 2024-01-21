<script setup lang="ts">
import { ref } from 'vue'
import { NPageHeader, NCard, NDivider, NText, NSpace, NSkeleton, NButton, NH6 } from 'naive-ui'

import router from '@/router'
import CustomerResponse from '@/components/CustomerResponse.vue'
import { useApi } from '@/composables/useApi'

interface TicketInformations {
  id: number
  messages: {
    message: string
    time: string
    selectedOption: string
    response: string
  }[]
  availableOptions: { name: string; description: string }[]
}

const props = defineProps<{ id: string }>()
const { fetch } = useApi()
const ticketInformations = ref<TicketInformations>()
const ticketUpdate = ref({ option: undefined, message: undefined })

const { isFetching } = fetch<TicketInformations>(`ticket/${props.id}`, {
  afterFetch(ctx: { data: TicketInformations }) {
    ticketInformations.value = ctx.data
    return ctx
  }
}).json()

const { isFetching: isAnswering, execute } = fetch<TicketInformations>(`ticket/${props.id}`, {
  immediate: false,
  afterFetch(ctx: { data: TicketInformations }) {
    ticketInformations.value = ctx.data
    return ctx
  }
})
  .post(ticketUpdate)
  .json()
</script>

<template>
  <n-page-header
    :title="`Ticket #${ticketInformations.id}`"
    v-if="ticketInformations"
    @back.prevent="router.push({ name: 'home' })"
  />
  <n-space vertical v-if="isFetching">
    <n-skeleton height="40px" width="100%" />
    <n-skeleton height="40px" width="60%" />
  </n-space>
  <n-space vertical v-if="ticketInformations">
    <n-card
      v-for="message in ticketInformations.messages"
      :title="message.selectedOption"
      :key="message.time"
      size="small"
    >
      <template #header-extra>
        <n-text type="info">{{ message.time }}</n-text>
      </template>
      <n-text>{{ message.message }}</n-text>
      <n-divider />
      <n-h6>Réponse du service client</n-h6>
      <n-text>{{ message.response }}</n-text>
    </n-card>
    <n-card title="Répondre" size="small" v-if="ticketInformations.availableOptions.length > 0">
      <customer-response :options="ticketInformations.availableOptions" v-model="ticketUpdate" />
      <n-button @click="execute()" :loading="isAnswering">Répondre</n-button>
    </n-card>
  </n-space>
</template>

<style scoped>
.n-text {
  white-space: pre-line;
  line-height: 3;
}
</style>
