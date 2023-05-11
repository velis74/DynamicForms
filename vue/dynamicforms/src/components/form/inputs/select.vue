<template>
  <vuetify-input
    :label="baseBinds.label"
    :messages="baseBinds.messages"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
  >
    <Multiselect
      v-model="selected"
      :options="options"
      :close-on-select="true"
      :clear-on-select="true"
      :hide-selected="false"
      :preserve-search="true"
      :preselect-first="false"
      label="text"
      track-by="id"

      :disabled="disabled"
      :multiple="multiple"
      :taggable="taggable"
      :aria-describedby="field.helpText && showLabelOrHelpText ? field.name + '-help' : null"
      :placeholder="field.placeholder"

      :options-limit="limit"
      :loading="loading"
      :internal-search="!field.ajax"

      @select="onSelect"
      @input="onInput"
      @tag="onTag"
      @search-change="onSearch"
    />
  </vuetify-input>
</template>

<script lang="ts">
/**
 * TODO: the field does not look like a Vuetify field: label is on left
 * TODO: There's no demo for AJAX loading. there is one, though in project-base (Impersonate user)
 */
import { defineComponent } from 'vue';
import Multiselect from 'vue-multiselect';

import apiClient from '../../util/api-client';
import TranslationsMixin from '../../util/translations-mixin';
import { DfForm } from '../namespace';

import InputBase from './base';
import VuetifyInput from './input-vuetify.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'DSelect',
  components: { Multiselect, VuetifyInput },
  mixins: [InputBase, TranslationsMixin],
  data() {
    return {
      selected: null as DfForm.ChoicesJSON | DfForm.ChoicesJSON[] | null,
      disabled: false,
      required: false,
      loadedChoices: [] as DfForm.ChoicesJSON[],
      loading: false,
      limit: 99999,
    };
  },
  computed: {
    options() { return this.field.choices || this.loadedChoices; },
    options_json() { return JSON.stringify(this.options); },
    multiple() { return this.field.renderParams.multiple; },
    taggable() { return this.field.renderParams.allowTags; },
    result: {
      get() {
        if (this.selected) {
          return this.multiple ?
            (<DfForm.ChoicesJSON[]> this.selected).map((i) => i.value) :
            (<DfForm.ChoicesJSON> this.selected).value;
        }
        return '';
      },
      set(value: any) {
        if (value != null) {
          if (this.multiple) {
            const val = value.constructor === Array ? value.map(String) : value.split(',');
            this.selected = this.options.filter((o) => val.includes(`${o.value}`));
          } else {
            const fnd = this.options.find((o) => String(o.value) === String(value));
            this.selected = fnd || null;
          }
        } else {
          this.selected = null;
        }
      },
    },
  },
  watch: {
    selected: function selectedChanged() {
      this.value = this.result;
    },
  },
  mounted: function mounted() {
    if (!this.multiple && !this.field.allowNull && !this.value && this.options.length) {
      // Auto select first element
      this.result = this.options[0].value;
    } else {
      this.result = this.value;
    }
  },
  methods: {
    onSelect() {
      this.value = this.result;
    },
    onInput(inp: any) {
      if (inp === null) {
        this.value = this.result;
      }
    },
    onTag(newTag: string) {
      const newTagObj = { value: newTag, text: newTag };
      this.field.choices.push(newTagObj);
      if (this.multiple) {
        (<DfForm.ChoicesJSON[]> this.selected).push(newTagObj);
      } else {
        this.selected = newTagObj;
      }
    },
    async onSearch(query: string) {
      const headers = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };
      const req = `${this.field.ajax.url_reverse}?${this.field.ajax.query_field}=${query}` +
        `${this.field.ajax.additional_parameters ? `&${this.field.ajax.additional_parameters}` : ''}`;
      this.loading = true;
      try {
        let loadedData = (await apiClient.get(req, { headers, params: this.filterData })).data;
        if (Array.isArray(loadedData)) {
          // Pagination was not delivered. We got a plain array
          loadedData = { results: loadedData, next: null };
        }
        this.loadedChoices = loadedData.results.map(
          (item: { [ key: string ]: any }) => ({
            id: item[this.field.ajax.value_field],
            text: item[this.field.ajax.text_field],
          }),
        );
        this.limit = loadedData.next ? this.loadedChoices.length : 99999;
      } finally {
        this.loading = false;
      }
    },
  },
});
</script>

<style src="~/vue-multiselect/dist/vue-multiselect.css"></style>
