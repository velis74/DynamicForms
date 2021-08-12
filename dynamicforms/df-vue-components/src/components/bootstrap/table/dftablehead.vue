<template>
  <thead>
  <tr>
    <th v-for="(col, idx) in columns" :key="col.name" :style="`text-align: ${col.alignment}`"
        :class="col.th_classes" @click="colClicked($event, col, idx)">
            {{ col.label }}
            <span v-if="col.isOrdered" class="ordering">
              <div class="ordering-arrow">{{ col.ascDescChar }}</div>
              {{ col.orderIndexChar }}
            </span>
    </th>
  </tr>
  <dftablefilterrow v-if="filter" :configuration="filter"
                    v-on:setTableFilter="setTableFilter"></dftablefilterrow>
  </thead>
</template>

<script>
import dftablefilterrow from '@/components/bootstrap/table/dftablefilterrow.vue';

export default {
  name: 'dftablehead',
  props: {
    columns: {
      type: Array,
      required: true,
    },
    filter: {
      type: Object,
    },
  },
  methods: {
    setTableFilter(filter) {
      this.$emit('setTableFilter', filter);
    },
  },
  components: {
    dftablefilterrow,
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
