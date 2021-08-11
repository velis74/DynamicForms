<template>
  <tr>
    {{ filter }}
    <th v-for="(column, idx) in columns" :key="idx">
      <dfformcolumn :key="idx" :def="{ field: column }" :data="filter" v-on:onValueConfirmed="onValueConfirmed"
                    :errors="{}" :showLabelOrHelpText="false"/>
    </th>
    {{ queryParams }}
  </tr>
</template>

<script>
import _ from 'lodash';
import dfformcolumn from '@/components/bootstrap/form/dfformcolumn.vue';
import DisplayMode from '@/logic/displayMode';

export default {
  name: 'dftablefilterrow',
  props: ['configuration'],
  mounted() {
    console.log(this.configuration);
  },
  data() {
    return {
      filter: {},
      queryParams: {},
    };
  },
  computed: {
    columns() {
      // todo: which columns are in filter needs to be configured in serializer......
      return _.filter(this.configuration.columns, (c) => c.visibility.table === DisplayMode.FULL
          && c.visibility.form === DisplayMode.FULL);
    },
  },
  methods: {
    onValueConfirmed(v) {
      console.log('value confirmed - TRigger FILTER');
      _.each(_.keys(v), (k) => {
        this.queryParams[k] = v[k];
      });
    },
  },
  components: {
    dfformcolumn,
  },
};
</script>

<style scoped>
th.ordering {
  cursor:      pointer;
  user-select: none;
}

th.ordering > span.ordering > div.ordering-arrow {
  font-size:   125%;
  line-height: .8em; /* increase font size for the arrow */
  display:     inline-block; /* but do not allow it to affect line size */
}
</style>
