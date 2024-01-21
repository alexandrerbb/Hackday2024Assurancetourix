<script setup lang="ts">
import { RouterView } from 'vue-router'
import {
  NConfigProvider,
  NMessageProvider,
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NGlobalStyle,
  type GlobalThemeOverrides
} from 'naive-ui'
// import { NThemeEditor } from 'naive-ui'

import AppNavbar from '@/components/AppNavbar.vue'

const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#D21312',
    primaryColorHover: '#D21312',
    primaryColorPressed: '#D21312',
    primaryColorSuppl: '#D21312',
    bodyColor: '#F4F4F4FF',
    fontSizeMini: '14px',
    fontSizeTiny: '14px',
    fontSizeSmall: '16px',
    fontSize: '16px',
    fontSizeMedium: '16px'
  },
  Form: {
    labelFontSizeTopMedium: '1rem'
  },
  Card: {
    titleFontSizeLarge: '1.25rem',
    titleFontSizeSmall: '1.25rem'
  },
  Message: {
    fontSize: '1rem'
  },
  PageHeader: {
    titleFontSize: '1.5rem',
    backSize: '1.5rem'
  }
}
</script>

<template>
  <!-- <n-theme-editor> -->
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-global-style />
      <n-layout>
        <n-layout-header>
          <app-navbar />
        </n-layout-header>
        <n-layout-content content-style="padding: 2rem;">
          <router-view />
        </n-layout-content>
      </n-layout>
    </n-message-provider>
  </n-config-provider>
  <!-- </n-theme-editor> -->
</template>

<style>
.n-page-header {
  margin-bottom: 1.5rem;
}
</style>
