<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <div
      :id="def.uuid"
      slot="input"
      :key="def.uuid"
      class="df-datetime-class"
      :name="def.name"
    >
      <div class="input-group mb-3">
        <datetime
          :key="datetimeFieldKey"
          v-model="value"
          type="datetime"
          :phrases="{ok: gettext('Ok'), cancel: gettext('Cancel')}"
          :input-class="'df-widget-datetime-input form-control'"
          :format="displayFormat"
          @input="dateTimeInput"
        />
        <div class="input-group-append">
          <button class="btn btn-sm btn-outline-secondary clear-datetime" type="button" @click="clear">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-trash"
              viewBox="0 0 16 16"
            >
              <path
                d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1
                0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
              />
              <path
                fill-rule="evenodd"
                d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1
                0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0
                1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </DFWidgetBase>
</template>

<script>
import { Datetime } from 'vue-datetime';

import DynamicForms from '../../../dynamicforms';
import translationsMixin from '../../../mixins/translationsMixin';

import DFWidgetBase from './dfwidgetbase.vue';

export default {
  name: 'DFWidgetDatetime',
  components: { DFWidgetBase, Datetime },
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
