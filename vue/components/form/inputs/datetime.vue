<template>
  <v-input v-bind="baseBinds">
    <datetime
      v-model="value"
      :type="inputType"
      :phrases="{ok: gettext('Ok'), cancel: gettext('Cancel')}"
      :input-class="'df-widget-datetime-input form-control'"
      :format="displayFormat"
      style="display: inline-block; float: left; width: 85%"
      @input="dateTimeInput"
    />
    <div class="input-group-append" style="display: inline-block; float: left; width: 15%;">
      <div
        class="btn btn-sm clear-datetime shadow-none input-group-text"
        type="button"
        style="border: none; justify-content: center;"
        @click="clear"
      >
        <IonIcon class="datetime-delete-icon" name="trash-outline"/>
      </div>
    </div>
  </v-input>
</template>

<script>
/**
 * TODO: the field does not look like a Vuetify field: it is not underlined, label is on left
 */
import { DateTime } from 'luxon';
import { Datetime } from 'vue-datetime';
import IonIcon from 'vue-ionicon';

import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';

const defaultDatetimeFormat = 'dd.MM.yyyy HH:mm:ss';

export default {
  name: 'DDateTime',
  components: { Datetime, IonIcon },
  mixins: [InputBase, TranslationsMixin],
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
      return this.field.renderParams.formFormat || defaultDatetimeFormat;
    },
  },
  methods: {
    onValueConfirmed(doFilter) { this.$emit('onValueConfirmed', doFilter); },
    dateTimeInput() { this.onValueConfirmed(true); },
    clear() { this.value = ''; },
  },
};
</script>

<style type="text/css">
@import '~vue-datetime/dist/vue-datetime.css';
</style>

<style scoped>
.datetime-delete-icon {
  width: 1em;
}
</style>
