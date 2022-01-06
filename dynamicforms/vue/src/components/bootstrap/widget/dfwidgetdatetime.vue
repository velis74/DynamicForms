<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <div
      :id="def.uuid"
      slot="input"
      :key="def.uuid"
      class="input-group df-datetime-class"
      :name="def.name"
    >
      <datetime
        :key="datetimeFieldKey"
        v-model="value"
        :type="inputType"
        :phrases="{ok: gettext('Ok'), cancel: gettext('Cancel')}"
        :input-class="'df-widget-datetime-input form-control'"
        :format="displayFormat"
        style="display: inline-block; float: left; width: 85%"
        @input="dateTimeInput"
      />
      <div
        class="input-group-append"
        style="display: inline-block; float: left; width: 15%;"
      >
        <div
          class="btn btn-sm clear-datetime shadow-none input-group-text"
          type="button"
          style="border: none; justify-content: center;"
          @click="clear"
        >
          <IonIcon name="trash-outline"/>
        </div>
      </div>
    </div>
  </DFWidgetBase>
</template>

<script>
import _ from 'lodash';
import { DateTime } from 'luxon';
import { Datetime } from 'vue-datetime';

import DynamicForms from '../../../dynamicforms';
import translationsMixin from '../../../mixins/translationsMixin';
import IonIcon from '../ionicon.vue';

import DFWidgetBase from './dfwidgetbase.vue';

export default {
  name: 'DFWidgetDatetime',
  components: { DFWidgetBase, Datetime, IonIcon },
  mixins: [translationsMixin],
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  data() {
    return {
      datetimeFieldKey: Math.round(Math.random() * 1000),
    };
  },
  computed: {
    inputType() {
      return this.def.render_params.input_type;
    },
    maxLength() {
      // eslint-disable-next-line no-bitwise
      return this.def.render_params.max_length || (1 << 24);
    },
    isTextArea() {
      return this.def.textarea === true;
    },
    value: {
      get: function get() {
        return this.data[this.def.name];
      },
      set: function set(newVal) {
        if (_.size(newVal) && this.inputType !== 'datetime') {
          // eslint-disable-next-line no-param-reassign
          newVal = this.inputType === 'date' ?
            DateTime.fromISO(newVal).toFormat('yyyy-MM-dd') : DateTime.fromISO(newVal).toFormat('HH:mm:ss');
        }
        this.data[this.def.name] = newVal; // eslint-disable-line
        return this.data[this.def.name];
      },
    },
    displayFormat() {
      return this.def.render_params && this.def.render_params.form_format ?
        this.def.render_params.form_format : DynamicForms.defaultDatetimeFormat;
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

<style type="text/css">
@import '~vue-datetime/dist/vue-datetime.css';

/*.df-widget-datetime-input {*/
/*  width: 100%;*/
/*  !*border: none;*!*/
/*  !*border-color: red;*!*/
/*  border: 1px solid #ced4da;*/
/*  border-radius: 0.25rem;*/
/*  !*height: 100%;*!*/
/*}*/

/*.vdatetime-popup__header {*/
/*  background-color: palegreen;*/
/*}*/
</style>
