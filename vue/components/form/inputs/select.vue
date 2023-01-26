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
      @select="onSelect"
      @input="onInput"
      @tag="onTag"
    />
  </vuetify-input>
</template>

<script lang="ts">
/**
 * TODO: the field does not look like a Vuetify field: label is on left
 */
import { defineComponent } from 'vue';
import Multiselect from 'vue-multiselect';

import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';
import VuetifyInput from './input-vuetify.vue';

export default /* #__PURE__ */ defineComponent({
  name: 'DSelect',
  components: { Multiselect, VuetifyInput },
  mixins: [InputBase, TranslationsMixin],
  data() {
    return {
      selected: null,
      disabled: false,
      required: false,
    };
  },
  computed: {
    options() { return this.field.choices; },
    options_json() { return JSON.stringify(this.options); },
    multiple() { return this.field.renderParams.multiple; },
    taggable() { return this.field.renderParams.allowTags; },
    result: {
      get() {
        if (this.selected) {
          return this.multiple ? this.selected.map((i) => i.id) : this.selected.id;
        }
        return '';
      },
      set(value) {
        if (value != null) {
          if (this.multiple) {
            const val = value.constructor === Array ? value.map(String) : value.split(',');
            this.selected = this.options.filter((o) => val.includes(`${o.id}`));
          } else {
            this.selected = this.options.find((o) => String(o.id) === String(value));
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
    if (!this.multiple && !this.field.allowNull && !this.value && this.options) {
      this.result = this.options[0].id;
    } else {
      this.result = this.value;
    }
  },
  methods: {
    onSelect() {
      this.value = this.result;
    },
    onInput(inp) {
      if (inp === null) {
        this.value = this.result;
      }
    },
    onTag(newTag) {
      const newTagObj = { id: newTag, text: newTag };
      this.field.choices.push(newTagObj);
      if (this.multiple) {
        this.selected.push(newTagObj);
      } else {
        this.selected = newTagObj;
      }
    },
  },
});
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
