<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <div style="width: 100%;">
      <Datetime
        :key="datetimeFieldKey"
        v-model="valueDate"
        :type="inputType"
        :phrases="{ ok: gettext('Ok'), cancel: gettext('Cancel') }"
        :format="displayFormat"
        style="float: left; width: 85%; border: 1px solid #e8e8e8; height: 2rem;"
        input-style="vertical-align: sub; width: 100%;"
        value-zone="local"
        @input="dateTimeInput"
      />
      <InputClearButton style="display: inline-block; width: 1rem; margin-top: 0.5rem;" @clearButtonPressed="clear"/>
    </div>
  </vuetify-input>
</template>

<script setup lang="ts">
import 'vue-datetime3/style.css';

import { DateTime } from 'luxon';
import { computed } from 'vue';
import { Datetime } from 'vue-datetime3';

import { useTranslations } from '../../util/translations-mixin';

import { BaseEmits, BaseProps, basePropsDefault, useInputBase } from './base';
import InputClearButton from './clear-input-button.vue';
import VuetifyInput from './input-vuetify.vue';

interface Props extends BaseProps {}
const props = withDefaults(defineProps<Props>(), basePropsDefault);

interface Emits extends BaseEmits {
  (e: 'onValueConfirmed', value: any): any
}
const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);
const { gettext } = useTranslations();

// data
let datetimeFieldKey = Math.round(Math.random() * 1000);

// computed
const inputType = computed(() => props.field.renderParams.inputType as 'datetime' | 'date' | 'time' | undefined);

const valueDate = computed({
  get: function get(): any {
    return props.modelValue;
  },
  set: function set(newVal: any) {
    if (newVal && props.field.renderParams.inputType !== 'datetime') {
      // eslint-disable-next-line no-param-reassign
      newVal = props.field.renderParams.inputType === 'date' ?
        DateTime.fromISO(newVal).toFormat('yyyy-MM-dd') : DateTime.fromISO(newVal).toFormat('HH:mm:ss');
    }
    emits('update:modelValue', newVal);
  },
});

const displayFormat = computed(() => props.field.renderParams.formFormat || 'dd.MM.yyyy HH:mm:ss');

// methods
function onValueConfirmed(doFilter: any) {
  emits('onValueConfirmed', doFilter);
}

function dateTimeInput() {
  onValueConfirmed(true);
}

function clear() {
  value.value = '';
  datetimeFieldKey = Math.round(Math.random() * 1000);
}

</script>

<style>
.vdatetime-calendar__month {
  white-space: normal;
}
</style>
