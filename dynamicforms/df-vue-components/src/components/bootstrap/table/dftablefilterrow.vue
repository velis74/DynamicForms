<template>
  <tr>
<!--    <th v-for="(column, idx) in columns" :key="idx">-->
<!--      <dfformcolumn :key="idx" :def="column" :data="null" :errors="null"/>-->
<!--    </th>-->
  </tr>
</template>

<script>
import _ from 'lodash';
// import dfformcolumn from '@/components/bootstrap/form/dfformcolumn.vue';

export default {
  name: 'dftablefilterrow',
  props: ['configuration'],
  mounted() {
    console.log(this.configuration, 999);
  },
  computed: {
    columns() {
      return _.map(this.configuration.columns, (c) => ({ field: c }));
    },
  },
  methods: {
  },
  components: {
    // dfformcolumn,
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
