<script setup lang="ts">
import AppNotification from './notifications/df-notifications.vue';
</script>

<template>
  <div>
    <app-notification/>
    <ModalView/>
    <slot/>
  </div>
</template>
