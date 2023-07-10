<template>
  <vuetify-input
    ref="multiselectRef"
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
      @open="multiSelectOpen"
      @close="multiSelectClose"
    >
      <template #singleLabel="props">
        <span v-if="props.option.icon">
          <IonIcon class="action-icon" :name="props.option.icon"/>
        </span>
        <span v-else>
          {{ props.option.text }}
        </span>
      </template>
      <template #option="props">
        <span v-if="props.option.icon">
          <IonIcon class="action-icon" :name="props.option.icon"/>
        </span>
        {{ props.option.text }}
      </template>
    </Multiselect>
    <div id="spacer-div" :style="`width:0px; height: ${minHeight}px; margin-top: ${dropdownTop}px`">&nbsp;</div>
  </vuetify-input>
</template>

<script lang="ts">
/**
 * TODO: the field does not look like a Vuetify field: label is on left
 * TODO: There's no demo for AJAX loading. there is one, though in project-base (Impersonate user)
 */
import { defineComponent, nextTick, ref } from 'vue';
import IonIcon from 'vue-ionicon';
import Multiselect from 'vue-multiselect';

import apiClient from '../../util/api-client';
import TranslationsMixin from '../../util/translations-mixin';
import { DfForm } from '../namespace';

import InputBase from './base';
import VuetifyInput from './input-vuetify.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'DSelect',
  components: { Multiselect, VuetifyInput, IonIcon },
  mixins: [InputBase, TranslationsMixin],
  setup() {
    const multiselectRef = ref<typeof VuetifyInput | null>(null);
    const minHeight = ref<number>(0);
    const dropdownTop = ref<number>(0);

    function multiSelectOpen() {
      nextTick(() => {
        const dropDown = multiselectRef.value?.$el.querySelector('.multiselect__content-wrapper');
        const spacerDiv = multiselectRef.value?.$el.querySelector('#spacer-div');
        const dialogParent = multiselectRef.value?.$el.closest('.v-card-text');
        const isDialog = multiselectRef.value?.$el.closest('.v-dialog');
        if (isDialog && dropDown.getBoundingClientRect().bottom > dialogParent.getBoundingClientRect().bottom) {
          minHeight.value = dropDown.getBoundingClientRect().bottom - dialogParent.getBoundingClientRect().bottom;
          dropdownTop.value = dropDown.getBoundingClientRect().top - spacerDiv.getBoundingClientRect().top;
        }
      });
    }

    function multiSelectClose() { minHeight.value = 0; dropdownTop.value = 0; }

    return { multiselectRef, minHeight, dropdownTop, multiSelectOpen, multiSelectClose };
  },
  data() {
    return {
      selected: null as DfForm.ChoicesJSON | DfForm.ChoicesJSON[] | null,
      required: false,
      loadedChoices: [] as DfForm.ChoicesJSON[],
      loading: false,
      limit: 99999,
    };
  },
  computed: {
    disabled() { return this.field.readOnly; },
    options() { return this.field.choices || this.loadedChoices; },
    options_json() { return JSON.stringify(this.options); },
    multiple() { return this.field.renderParams.multiple; },
    taggable() { return this.field.renderParams.allowTags; },
    result: {
      get() {
        if (this.selected) {
          return this.multiple ?
            (<DfForm.ChoicesJSON[]> this.selected).map((i) => i.id) :
            (<DfForm.ChoicesJSON> this.selected).id;
        }
        return '';
      },
      set(value: any) {
        if (value != null) {
          if (this.multiple) {
            const val = value.constructor === Array ? value.map(String) : value.split(',');
            this.selected = this.options.filter((o) => val.includes(`${o.id}`));
          } else {
            const fnd = this.options.find((o) => String(o.id) === String(value));
            this.selected = fnd || null;
          }
        } else {
          this.selected = null;
        }
      },
    },
  },
  watch: {
    selected() {
      this.onSelect();
    },
  },
  async mounted() {
    if (!this.multiple && !this.field.allowNull && !this.value && this.options.length) {
      // Auto select first element
      this.result = this.options[0].id;
    } else {
      this.result = this.value;
    }
    if (this.field.ajax && this.value) {
      console.log(this.field.ajax.value_field, this.value);
      await this.queryOptions(this.value, this.field.ajax.value_field);
      this.result = this.loadedChoices[0]?.id;
    }
  },
  methods: {
    onSelect() {
      if (!this.field.readOnly) {
        this.value = this.result;
      }
    },
    onInput(inp: any) {
      if (inp === null) {
        this.value = this.result;
      }
    },
    onTag(newTag: string) {
      const newTagObj: DfForm.ChoicesJSON = { id: newTag, text: newTag };
      this.field.choices.push(newTagObj);
      if (this.multiple) {
        (<DfForm.ChoicesJSON[]> this.selected).push(newTagObj);
      } else {
        this.selected = newTagObj;
      }
    },
    async queryOptions(query: string, query_field: string): Promise<void> {
      const headers = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };
      const req = `${this.field.ajax.url_reverse}?${query_field}=${query}` +
        `${this.field.ajax.additional_parameters ? `&${this.field.ajax.additional_parameters}` : ''}`;
      this.loading = true;
      try {
        let loadedData = (await apiClient.get(req, { headers, params: this.filterData })).data;
        if (Array.isArray(loadedData)) {
          // Pagination was not delivered. We got a plain array
          loadedData = { results: loadedData, next: null };
        }
        this.loadedChoices = loadedData.results.map(
          (item: { [ key: string ]: any }): DfForm.ChoicesJSON => ({
            id: item[this.field.ajax.value_field],
            text: item[this.field.ajax.text_field],
          }),
        );
        this.limit = loadedData.next ? this.loadedChoices.length : 99999;
      } finally {
        this.loading = false;
      }
    },
    async onSearch(query: string) {
      if (this.field.ajax) {
        await this.queryOptions(query, this.field.ajax.query_field);
      }
    },
  },
});
</script>

<style src="~/vue-multiselect/dist/vue-multiselect.css"></style>
