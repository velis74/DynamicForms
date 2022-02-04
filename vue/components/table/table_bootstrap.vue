<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <component :is="'style'" :key="tableStyle" v-html="tableStyle"/>
      <div :class="uniqueId">
        <BootstrapTHead :rendered-columns="renderedColumns" @render-measured="measureRenders"/>
        <BootstrapTBody
          :data-columns="dataColumns"
          :rendered-columns="renderedColumns"
          :rows="rows"
          pk-name="pkName"
          @render-measured="measureRenders"
        />
        <!--BootstrapTFoot/-->
      </div>
    </v-card-text>
  </v-card>
</template>
<script>
import Table from './table';
import BootstrapTBody from './tbody_generic';
import BootstrapTHead from './thead_generic';

export default {
  name: 'BootstrapTable',
  components: { BootstrapTHead, BootstrapTBody },
  mixins: [Table],
};
</script>
