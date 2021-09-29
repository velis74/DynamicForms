<template>
  <DFWidgetBase :def="def" :data="data" :errors="errors" :show-label-or-help-text="showLabelOrHelpText">
    <input
      :id="def.uuid"
      slot="input"
      type="file"
      :class="def.render_params.field_class"
      :name="def.name"
      :aria-describedby="def.help_text && showLabelOrHelpText ? def.name + '-help' : null"
      :readonly="def.read_only === true"
      :disabled="def.read_only === true"
      @change="change"
    >
  </DFWidgetBase>
</template>

<script>
import _ from 'lodash';
import { v4 as uuidv4 } from 'uuid';

import DFWidgetBase from './dfwidgetbase.vue';

import apiClient from '@/apiClient';

export default {
  name: 'DFWidgetFile',
  components: { DFWidgetBase },
  props: {
    def: { type: Object, required: true },
    data: { type: Object, required: true },
    errors: { type: Object, required: true },
    showLabelOrHelpText: { type: Boolean, default: true },
  },
  methods: {
    change(evt) {
      console.log(evt.currentTarget.files);
      const fileIdentifier = `fl_${uuidv4()}`;

      const formData = new FormData();

      if (!evt.currentTarget.files.length) return;

      _.each(evt.currentTarget.files, (f) => {
        formData.append('file', f, fileIdentifier);
      });

      // upload file
      apiClient.post('/dynamicforms/preupload-file/', formData).then((res) => {
        console.log(res);
      }).catch((err) => {
        console.log(err);
      });

      // this.data[this.def.name] = evt.currentTarget.files;  // eslint-disable-line
      this.data[this.def.name] = fileIdentifier;   // eslint-disable-line
    },
  },
};
</script>
