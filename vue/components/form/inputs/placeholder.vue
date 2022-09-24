<template>
  <v-input v-bind="baseBinds">
    <v-alert type="warning">
      Table-type nested serializers not supported for direct rendering yet. Please create your own
      <b>as_component_def_table()</b> function and appropriate <b>visual component</b>.
    </v-alert>
  </v-input>
</template>

<script>
import TranslationsMixin from '../../util/translations-mixin';

import InputBase from './base';

export default {
  name: 'DPlaceholder',
  mixins: [InputBase, TranslationsMixin],
};
</script>
