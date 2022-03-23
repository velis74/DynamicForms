<template>
  <vuetify-input :config="baseBinds">
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

<script>
/**
 * TODO: the field does not look like a Vuetify field: label is on left
 */
import Multiselect from 'vue-multiselect';

import TranslationsMixin from '../../util/translations_mixin';

import InputBase from './base';
import VuetifyInput from './input_vuetify';

export default {
  name: 'DSelect',
  components: { Multiselect, VuetifyInput },
  mixins: [InputBase, TranslationsMixin],
  data() {
    return {
      selected: null,
      disabled: false,
      required: false,
      selenium: true, // todo: this should be set globally, not per-component. and declared at top of html itself
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
      this.value = this.result; // eslint-disable-line vue/no-mutating-props
    },
  },
  mounted: function mounted() {
    if (!this.multiple && !this.field.allowNull && !this.value && this.options) {
      this.result = this.options[0].id;
    } else {
      this.result = this.value;
    }
    if (this.selenium) {
      window[`setSelectValue ${this.field.uuid}`] = (value) => {
        this.result = value;
      };
    }
  },
  destroyed: function destroyed() {
    if (this.selenium) {
      delete window[`setSelectValue ${this.field.uuid}`];
    }
  },
  methods: {
    onSelect(v) {
      this.value = this.result; // eslint-disable-line vue/no-mutating-props
      this.$emit('itemSelected', v);
      this.$emit('onValueConfirmed', true);
    },
    onInput(inp) {
      if (inp === null) {
        this.value = this.result; // eslint-disable-line vue/no-mutating-props
        this.$emit('itemSelected', inp);
      }
    },
    onTag(newTag) {
      const newTagObj = { id: newTag, text: newTag };
      this.field.choices.push(newTagObj); // eslint-disable-line vue/no-mutating-props
      if (this.multiple) {
        this.selected.push(newTagObj);
      } else {
        this.selected = newTagObj;
      }
    },
  },
};
</script>

<style scoped>
@import '~vue-multiselect/dist/vue-multiselect.min.css';
</style>
