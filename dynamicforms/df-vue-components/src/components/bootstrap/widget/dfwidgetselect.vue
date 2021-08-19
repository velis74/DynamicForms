<template>
  <dfwidgetbase :def="def" :data="data" :errors="errors" :showLabelOrHelpText="showLabelOrHelpText">
    <div slot="input" class="df-select-class" :id="def.uuid" :key="def.uuid" :name="def.name"
         :data-value="selenium ? result : null">
      <multiselect
          v-model="selected" :options="options" :close-on-select="true" :clear-on-select="true"
          :hide-selected="false" :preserve-search="true" :preselect-first="false"
          label="text" track-by="id"

          :disabled="disabled" :multiple="multiple"
          :aria-describedby="def.help_text && showLabelOrHelpText ? def.field_name + '-help' : null"
          :placeholder="def.placeholder"
          @select="onSelect" @input="onInput"
      />
    </div>
  </dfwidgetbase>
</template>

<script>
import dfwidgetbase from '@/components/bootstrap/widget/dfwidgetbase.vue';
import Multiselect from 'vue-multiselect';

export default {
  name: 'dfwidgetselect',
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  data() {
    return {
      selected: null,
      disabled: false,
      required: false,
      selenium: true, // todo: this should be set globally, not per-component. and declared at top of html itself
    };
  },
  computed: {
    options() { return this.def.choices; },
    multiple() { return this.def.render_params.multiple; },
    result: {
      get() {
        if (this.selected) {
          return this.multiple ? this.selected.map((i) => i.id) : this.selected.id;
        }
        return '';
      },
      set(value) {
        if (value) {
          if (this.multiple) {
            this.selected = this.options.filter((o) => value.split(',').includes(`${o.id}`));
          } else {
            this.selected = this.options.find((o) => o.id === value);
          }
        } else {
          this.selected = null;
        }
      },
    },
  },
  emits: ['update:modelValue'],
  mounted: function mounted() {
    if (!this.multiple && !this.def.allow_null && !this.data[this.def.name] && this.options) {
      this.result = this.options[0].id;
    } else {
      this.result = this.data[this.def.name];
    }
    if (this.selenium) {
      console.log(`setSelectValue ${this.def.uuid}`);
      window[`setSelectValue ${this.def.uuid}`] = (value) => {
        this.result = value;
      };
    }
  },
  destroyed: function destroyed() {
    if (this.selenium) {
      delete window[`setSelectValue ${this.def.uuid}`];
    }
  },
  methods: {
    onSelect(v) {
      this.data[this.def.name] = this.result; // eslint-disable-line vue/no-mutating-props
      this.$emit('itemSelected', v);
      this.$emit('onValueConfirmed', true);
    },
    onInput(inp) {
      if (inp === null) {
        this.data[this.def.name] = this.result; // eslint-disable-line vue/no-mutating-props
        this.$emit('itemSelected', inp);
      }
    },
  },
  watch: {
    selected: function selectedChanged() {
      this.data[this.def.name] = this.result; // eslint-disable-line vue/no-mutating-props
    },
  },
  components: {
    dfwidgetbase, Multiselect,
  },
};
</script>

<style scoped>
@import '~vue-multiselect/dist/vue-multiselect.min.css';
</style>
