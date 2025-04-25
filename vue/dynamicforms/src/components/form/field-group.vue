<template>
  <v-col :class="cssClasses + columnClasses">
    <v-card>
      <v-card-title v-if="field.title">
        <span class="float-left pt-2">
          {{ field.title }}
        </span>
        <v-switch
          v-if="props.field.name"
          v-model="use"
          class="float-right"
          color="primary"
          density="compact"
        />
      </v-card-title>
      <v-expand-transition>
        <template v-if="use">
          <v-card-text>
            <df-form-layout
              :is="field.componentName"
              :layout="field.layout"
              :payload="formPayload"
              :actions="actions"
              :errors="errors"
              :sub-handlers="subHandlers"
              :dialog-sub-handlers="dialogSubHandlers"
              transition="scale-transition"
            />
          </v-card-text>
        </template>
      </v-expand-transition>
    </v-card>
  </v-col>
</template>
<script setup lang="ts">
import { ComponentPublicInstance, computed, getCurrentInstance, inject, Ref, ref, watch } from 'vue';

import { dispatchAction } from '../actions/action-handler-mixin';
import FilteredActions from '../actions/filtered-actions';

import FormPayload from './definitions/form-payload';
import { Group } from './definitions/layout';

const props = withDefaults(
  defineProps<{
    field: Group,
    actions: FilteredActions,
    errors: Object,
    showLabelOrHelpText?: boolean,
    cssClasses?: string,
    subHandlers?: any,
    dialogSubHandlers?: any,
  }>(),
  {
    showLabelOrHelpText: true,
    cssClasses: '',
    subHandlers: undefined,
    dialogSubHandlers: undefined,
  },
);

const payload = inject<Ref<FormPayload>>('payload', ref({}) as Ref<FormPayload>);
const use = ref(false);
let formPayload = ref<FormPayload>();

const columnClasses = computed(
  () => { const classes = props.field.widthClasses; return classes ? ` ${classes} ` : ''; },
);

if (props.field.name == null) {
  use.value = true;
  formPayload = payload; // eslint-disable-line
} else {
  use.value = !(payload.value[props.field.name] == null);
  formPayload.value = FormPayload.create(payload.value[props.field.name] ?? {}, props.field.layout);
  const self = getCurrentInstance()?.proxy as ComponentPublicInstance;
  watch(use, (value) => { payload.value[props.field.name] = value ? formPayload.value : undefined; });
  watch(formPayload, (newValue: Object, oldValue: Object) => {
    payload.value[props.field.name] = use.value ? { ...newValue } : undefined;

    dispatchAction(self, props.actions.valueChanged, { field: props.field.name, oldValue, newValue });
  }, { deep: true });
}
</script>

<style>
label {
  margin-inline-end: .5em;
}
</style>
