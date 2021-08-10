<template>
  <dfwidgetbase :def="def" :data="data" :errors="errors">
    <multiselect
        slot="input"
        v-model="selected" :options="options" :close-on-select="true" :clear-on-select="true"
        :hide-selected="false" :preserve-search="true" :preselect-first="false"
        label="text" track-by="id"

        :id="def.uuid" :name="def.field_name" :disabled="disabled"
        :aria-describedby="def.help_text ? def.field_name + '-help' : null" :placeholder="def.placeholder"
        @select="onSelect" @input="onInput"
    />
  </dfwidgetbase>
</template>

<script>
import dfwidgetbase from '@/components/bootstrap/widget/dfwidgetbase.vue';
import Multiselect from 'vue-multiselect';

export default {
  name: 'dfwidgetselect',
  data() {
    return {
      selected: null,
      disabled: false,
      required: false,
    };
  },
  computed: {
    options() { return this.def.choices; },
    result: {
      get() { return this.selected ? this.selected.id : null; },
      set(value) { this.selected = this.options.find((o) => o.id === value); },
    },
  },
  emits: ['update:modelValue'],
  props: {
    def: {
      type: Object,
      required: true,
    },
    data: {
      type: Object,
      required: true,
    },
    errors: {
      type: Object,
      required: true,
    },
  },
  methods: {
    onSelect(v) {
      this.$emit('itemSelected', v);
    },
    onInput(inp) {
      if (inp === null) {
        this.$emit('itemSelected', inp);
      }
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
