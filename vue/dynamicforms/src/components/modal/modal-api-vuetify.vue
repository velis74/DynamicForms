<template>
  <!--https://stackoverflow.com/questions/55085735/vuetify-v-dialog-dynamic-width-->
  <v-dialog
    v-model="doShow"
    :width="computedWidth"
    :max-width="computedWidth"
    :fullscreen="computedFullScreen"
    persistent
  >
    <v-card>
      <v-card-title>
        <slot name="title"/>
      </v-card-title>
      <v-card-text>
        <slot name="body"/>
      </v-card-text>
      <v-card-actions>
        <div style="flex:1">
          <slot name="actions"/>
        </div>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import { defaultActionHandler } from '../actions/action';
import { useActionHandler } from '../actions/action-handler-composable';

import DialogSize from './definitions/dialog-size';

export default /* #__PURE__ */ defineComponent({
  name: 'VuetifyModalDialog',
  props: {
    show: { type: Boolean, default: () => false },
    options: { type: Object, required: true }, // dialogOptions
  },
  setup() {
    const { handler } = useActionHandler();
    return { handler };
  },
  data() {
    return {
      doShow: this.show,
      fullScreen: false,
    };
  },
  computed: {
    size() { return this.options.size; },
    computedWidth() {
      if (this.computedFullScreen) return 'unset';
      switch (this.size) {
      case DialogSize.SMALL:
        return 400;
      case DialogSize.MEDIUM:
        return 600;
      case DialogSize.LARGE:
        return 800;
      case DialogSize.X_LARGE:
        return 1140;
      default:
        return 'unset';
      }
    },
    computedFullScreen() {
      if (this.size === DialogSize.SMALL && !this.$vuetify.display.smAndUp) return true;
      if (this.size === DialogSize.MEDIUM && !this.$vuetify.display.mdAndUp) return true;
      if (this.size === DialogSize.LARGE && !this.$vuetify.display.lgAndUp) return true;
      if (this.size === DialogSize.X_LARGE && !this.$vuetify.display.xl) return true;
      return false;
    },
  },
  mounted() {
    this.handler
      .register('cancel', defaultActionHandler)
      .register('close', defaultActionHandler)
      .register('submit', defaultActionHandler)
      .register('delete_dlg', defaultActionHandler);
  },
});
</script>
