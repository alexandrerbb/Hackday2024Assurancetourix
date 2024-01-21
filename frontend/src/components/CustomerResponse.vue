<script setup lang="ts">
import { NForm, NFormItem, NSelect, NInput } from 'naive-ui'

interface TicketUpdate {
  message?: string
  option?: string
}

const props = defineProps<{
  options: { name: string; description?: string }[]
  modelValue: TicketUpdate
}>()
const emit = defineEmits(['update:modelValue'])
</script>
<template>
  <n-form>
    <n-form-item path="option">
      <n-select
        :options="props.options"
        value-field="name"
        label-field="description"
        placeholder="Sélectionner une réponse."
        :value="props.modelValue.option"
        :on-update:value="(n) => emit('update:modelValue', { ...props.modelValue, option: n })"
      />
    </n-form-item>
    <n-form-item label="Votre message" path="message">
      <n-input
        :value="props.modelValue.message"
        type="textarea"
        placeholder="Message."
        :on-update:value="(n) => emit('update:modelValue', { ...props.modelValue, message: n })"
      />
    </n-form-item>
  </n-form>
</template>
