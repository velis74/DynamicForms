<template>
  <vuetify-input :config="baseBinds">
    <div style="width: 100%;">
      <datetime
        :key="datetimeFieldKey"
        v-model="value"
        :type="inputType"
        :phrases="{ok: gettext('Ok'), cancel: gettext('Cancel')}"
        :format="displayFormat"
        style="display: inline-block; float: left; width: 85%; border: 1px solid #e8e8e8; height: 2em;"
        input-style="vertical-align: sub; width: 100%;"
        @input="dateTimeInput"
      />
      <div style="display: inline-block; float: left; width: 15%;">
        <div
          type="button"
          style="border: none; justify-content: center;"
          @click="clear">
          <IonIcon class="datetime-delete-icon" name="trash-outline"/>
        </div>
      </div>
    </div>
  </vuetify-input>
</template>

<script>
import { DateTime } from 'luxon';
import { Datetime } from 'vue-datetime';
import IonIcon from 'vue-ionicon';

import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';
import VuetifyInput from './input_vuetify';

export default {
  name: 'DDatetime',
  components: { Datetime, IonIcon, VuetifyInput },
  mixins: [InputBase, TranslationsMixin],
  data() {
    return { datetimeFieldKey: Math.round(Math.random() * 1000) };
  },
  computed: {
    inputType() {
      return this.field.renderParams.inputType;
    },
    value: {
      get: function get() {
        return this.payload.value;
      },
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
    onValueConfirmed(doFilter) {
      this.$emit('onValueConfirmed', doFilter);
    },
    dateTimeInput() {
      this.onValueConfirmed(true);
    },
    clear() {
      this.value = '';
      this.datetimeFieldKey = Math.round(Math.random() * 1000);
    },
  },
};
</script>

<style scoped>
@import '~vue-datetime/dist/vue-datetime.css';

.datetime-delete-icon {
  width: 1em;
  top: 55%;
  position: absolute;
  margin: 0;
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
}
</style>
