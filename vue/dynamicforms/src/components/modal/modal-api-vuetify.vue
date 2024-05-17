<script setup lang="ts">
import { computed, ref } from 'vue';
import { useDisplay } from 'vuetify';

import { useActionHandler } from '../actions/action-handler-composable';
import type { ActionsNS } from '../actions/namespace';

import DialogSize from './definitions/dialog-size';

type IHandlers = ActionsNS.IHandlers;

interface Props {
  show: boolean,
  options: any,
  actionHandlers?: IHandlers
}

const props = withDefaults(defineProps<Props>(), { show: false, actionHandlers: undefined });

const { handler } = useActionHandler();
for (const key of Object.keys(props.actionHandlers || {})) {
  if (props.actionHandlers?.[key]) handler.register(key, props.actionHandlers[key]);
}

const display = useDisplay();

const size = computed<DialogSize>(() => props.options.size);

const doShow = ref<boolean>(props.show);

const fullScreen = computed(() => {
  if (size.value === DialogSize.SMALL && !display.smAndUp.value) return true;
  if (size.value === DialogSize.MEDIUM && !display.mdAndUp.value) return true;
  if (size.value === DialogSize.LARGE && !display.lgAndUp.value) return true;
  return size.value === DialogSize.X_LARGE && !display.xl.value;
});

const width = computed<'unset' | number>(() => {
  if (fullScreen.value) return 'unset';
  switch (size.value) {
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
});

</script>

<template>
  <!--https://stackoverflow.com/questions/55085735/vuetify-v-dialog-dynamic-width-->
  <v-dialog
    v-model="doShow"
    :width="width"
    :max-width="width"
    :fullscreen="fullScreen"
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
