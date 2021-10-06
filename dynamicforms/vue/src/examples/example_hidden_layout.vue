<template>
  <div>
    <DFFormLayout :rows="rows" :uuid="uuid" :record="record" @unit-changed="unitChanged" @note-changed="noteChanged"/>
  </div>
</template>

<script>
import DFFormLayout from '../components/bootstrap/form/dfformlayout.vue';
import DisplayMode from '../logic/displayMode';

export default {
  name: 'ExampleHiddenLayout',
  components: { DFFormLayout },
  props: {
    rows: { type: Array, required: true },
    uuid: { type: String, required: true },
    record: { type: Object, required: true },
  },
  computed: {
    fields() {
      const res = {};
      this.rows.forEach((row) => {
        row.forEach((column) => {
          res[column.field.name] = column.field;
        });
      });
      return res;
    },
    unitVisible() { return this.fields.unit.visibility.form === DisplayMode.FULL; },
  },
  mounted() { this.unitChanged({ newRec: this.record }); },
  methods: {
    noteChanged(payload) {
      this.fields.unit.visibility.form = payload.newRec.note === 'abc' ? DisplayMode.HIDDEN : DisplayMode.FULL;
      // TODO this is probably bad: we're not changing unit value, but we ARE changing its visibility, so it would make
      //  sense to somehow run unitChanged automatically... Perhaps we should watch its definition too, not just value
      this.unitChanged(payload);
    },
    unitChanged(payload) {
      const newRec = payload.newRec;

      const showField = (field, show) => {
        field.visibility.form = show ? DisplayMode.FULL : DisplayMode.HIDDEN;
      };

      showField(this.fields.int_fld, this.unitVisible && ['pcs', 'cst'].includes(newRec.unit));
      showField(this.fields.qty_fld, this.unitVisible && newRec.unit === 'wt');
      showField(this.fields.cst_fld, this.unitVisible && newRec.unit === 'cst');
    },
  },
};
</script>
