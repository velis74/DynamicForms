<template>
  <dfwidgetbase :def="def" :data="data" :errors="errors">
    <select slot="input" class="form-control" :id="def.uuid" :name="name"
            :disabled="disabled" :required="required">
      <option selected="selected">orange</option>
      <option>white</option>
      <option>purple</option>
    </select>
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
    errors: {
      type: Object,
      required: true,
    },
  },
  methods: {
    setOption(val = []) {
      this.select2.empty();
      this.select2.select2({
        placeholder: this.placeholder,
        ...this.settings,
        data: val,
        dropdownParent: $('.df-modal-handler'),
        tags: true,
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
    this.options = [{
      id: 1,
      text: 'Option 1',
    },
    {
      id: 2,
      text: 'Option 2',
    }];
    this.select2 = $(this.$el)
        .find('select')
        .select2({
          placeholder: this.placeholder,
          ...this.settings,
          data: this.options,
          tags: true,
          dropdownParent: $('.df-modal-handler'),
        }).on('select2:select select2:unselect', (ev) => {
          this.$emit('update:modelValue', this.select2.val());
          this.$emit('select', ev.params.data);
        });
    this.setValue(this.modelValue);

    setTimeout(() => {
      this.options = [{
        id: 6,
        text: 'Option 6',
      },
      {
        id: 5,
        text: 'Option 5',
      },
      {
        id: 7,
        text: 'Option 7',
      }];
      this.modelValue = 5;
    }, 3000);
  },
  beforeUnmount() {
    this.select2.select2('destroy');
  },
  components: {
    dfwidgetbase,
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
};
</script>

<style scoped>

</style>
