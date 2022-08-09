<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <div style="width: 100%;">
      <datetime
        :key="datetimeFieldKey"
        v-model="value"
        :type="inputType"
        :phrases="{ok: gettext('Ok'), cancel: gettext('Cancel')}"
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

<script>
import { DateTime } from 'luxon';
import { Datetime } from 'vue-datetime';

import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';
import InputClearButton from './clear_input_button';
import VuetifyInput from './input_vuetify';

export default {
  name: 'DDatetime',
  components: { Datetime, VuetifyInput, InputClearButton },
  mixins: [InputBase, TranslationsMixin],
  data() {
    return { datetimeFieldKey: Math.round(Math.random() * 1000) };
  },
  computed: {
    inputType() {
      return this.field.renderParams.inputType;
    },
    value: {
      get: function get() { return this.payload.value; },
      set: function set(newVal) {
        if (newVal && this.inputType !== 'datetime') {
          // eslint-disable-next-line no-param-reassign
          newVal = this.inputType === 'date' ?
            DateTime.fromISO(newVal).toFormat('yyyy-MM-dd') : DateTime.fromISO(newVal).toFormat('HH:mm:ss');
        }
        this.payload.setValue(newVal);
      },
    },
    displayFormat() {
      return this.field.renderParams.formFormat || 'dd.MM.yyyy HH:mm:ss';
    },
  },
  methods: {
    onValueConfirmed(doFilter) { this.$emit('onValueConfirmed', doFilter); },
    dateTimeInput() { this.onValueConfirmed(true); },
    clear() {
      this.value = '';
      this.datetimeFieldKey = Math.round(Math.random() * 1000);
    },
  },
};
</script>

<style scoped>
@import '~vue-datetime/dist/vue-datetime.css';
</style>
