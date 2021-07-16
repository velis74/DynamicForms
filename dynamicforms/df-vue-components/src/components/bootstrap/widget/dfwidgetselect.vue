<template>
  <dfwidgetbase :def="def" :data="data">
    <select slot="input" class="form-control" :id="id" :name="name"
            :disabled="disabled" :required="required"></select>
  </dfwidgetbase>
</template>

<script>
import dfwidgetbase from '@/components/bootstrap/widget/dfwidgetbase.vue';
import * as $ from 'jquery';
import 'select2/dist/js/select2.full';
import 'select2/dist/css/select2.min.css';

export default {
  name: 'dfwidgetselect',
  data() {
    return {
      select2: null,
      // properties bellow must be parsed from data or def object in on moounted
      id: '',
      name: '',
      placeholder: '',
      options: [],
      modelValue: null, // [String, Array]
      disabled: false,
      required: false,
      settings: {}, // configurable settings, see Select2 options API,
      // example: setting: { settingOption: value, settingOption: value }
    };
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
  },
  watch: {
    options: {
      handler(val) {
        this.setOption(val);
      },
      deep: true,
    },
    modelValue: {
      handler(val) {
        this.setValue(val);
      },
      deep: true,
    },
  },
  methods: {
    setOption(val = []) {
      this.select2.empty();
      this.select2.select2({
        placeholder: this.placeholder,
        ...this.settings,
        data: val,
      });
      this.setValue(this.modelValue);
    },
    setValue(val) {
      if (val instanceof Array) {
        this.select2.val([...val]);
      } else {
        this.select2.val([val]);
      }
      this.select2.trigger('change');
    },
  },
  mounted() {
    this.select2 = $(this.$el)
      .find('select')
      .select2({
        placeholder: this.placeholder,
        ...this.settings,
        data: this.options,
      })
      .on('select2:select select2:unselect', (ev) => {
        this.$emit('update:modelValue', this.select2.val());
        this.$emit('select', ev.params.data);
      });
    this.setValue(this.modelValue);
  },
  beforeUnmount() {
    this.select2.select2('destroy');
  },
  components: {
    dfwidgetbase,
  },
};
</script>

<style scoped>

</style>
