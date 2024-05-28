<script setup lang="ts">
// https://www.npmjs.com/package/vue-notification is the library used for notification
withDefaults(defineProps<{
  width?: number,
  position?: string,
}>(), {
  width: 350,
  position: 'top center',
});
</script>

<template>
  <notifications :width="width" :position="position">
    <template #body="{ item, close }">
      <div
        class="vue-notification"
        :class="item.type"
        @click="item.data.onNotificationClose(item, close, true)"
      >
        <div>
          <div
            v-if="item.data.duration === -1"
            style="display: inline-block; float: right; vertical-align: middle;"
          >
            <button
              type="button"
              class="close"
              @click="item.data.onNotificationClose(item, close)"
            >
              <v-icon icon="mdi-window-close"/>
            </button>
          </div>
          <div style="display: inline-block; max-width: 95%;" class="notification-title">
            <div v-html="item.title"/>
          </div>
          <div style="display: inline-block; max-width: 95%;" class="notification-content">
            <div style="margin-left: 0.4em;" v-html="item.text"/>
          </div>
        </div>
      </div>
    </template>
  </notifications>
</template>
