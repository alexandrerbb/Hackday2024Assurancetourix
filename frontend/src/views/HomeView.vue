<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { NPageHeader, NButton, NDataTable } from 'naive-ui'
import type { RowData } from 'naive-ui/es/data-table/src/interface'

import { useApi } from '@/composables/useApi'
import router from '@/router'

const { fetch } = useApi()

const columns = [
  { title: 'Date', key: 'date' },
  { title: 'Message', key: 'lastMessage' },
  { title: 'Réponse', key: 'lastResponse' }
]

const { data, isFetching } = fetch('').json()

const rowProps = (row: RowData) => {
  return {
    style: 'cursor: pointer;',
    onClick: () => {
      router.push({ name: 'ticket', params: { id: row.id } })
    }
  }
}
</script>

<template>
  <n-page-header title="Mes tickets">
    <template #extra>
      <router-link to="/new"><n-button>Nouveau ticket</n-button></router-link>
    </template>
  </n-page-header>
  <n-data-table
    :data="data"
    v-if="data"
    :bordered="true"
    :columns="columns"
    :loading="isFetching"
    :row-props="rowProps"
  />
</template>
