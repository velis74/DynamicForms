<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-card-text>
      <component :is="'style'" :key="tableStyle" v-html="tableStyle"/>
      <div :class="uniqueId">
        <VuetifyTHead :rendered-columns="renderedColumns" @render-measured="measureRenders"/>
        <VuetifyTBody
          :data-columns="dataColumns"
          :rendered-columns="renderedColumns"
          :rows="rows"
          pk-name="pkName"
          @render-measured="measureRenders"
        />
        <!--VuetifyTFoot/-->
      </div>
    </v-card-text>
  </v-card>
</template>
<script>
import Table from './table';
import VuetifyTBody from './tbody_vuetify';
import VuetifyTHead from './thead_vuetify';

export default {
  name: 'VuetifyTable',
  components: { VuetifyTHead, VuetifyTBody },
  mixins: [Table],
};
</script>
