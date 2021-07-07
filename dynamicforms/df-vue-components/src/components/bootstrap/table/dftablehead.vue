<template>
  <thead>
  <tr>
    <th v-for="(col, idx) in columns" :key="col.name" :style="`text-align: ${col.align}`"
        :class="col.th_classes" @click="colClicked($event, col, idx)">
            {{ col.label }}
            <span v-if="col.isOrdered" class="ordering">
              <div class="ordering-arrow">{{ col.ascDescChar }}</div>
              {{ col.orderIndexChar }}
            </span>
    </th>
  </tr>
  </thead>
</template>

<script>
export default {
  name: 'dftablehead',
  props: ['columns'],
  computed: {
    numSortedCols() {
      return this.columns.filter((col) => col.ordering.includes('seg-')).length;
    },
  },
  methods: {
    colClicked(event, column, colIdx) {
      if (!column.isOrdered) {
        // don't do anything if this column is not sortable
        return;
      }
      if (event.altKey) {
        // Show dialog with sort order options
      } else if (event.ctrlKey && event.shiftKey) {
        // remove column from ordering
        column.setSorted('unsorted');
      } else if (event.ctrlKey) {
        // set column as first sorted column
        this.$parent.$parent.changeOrder(colIdx, column.isDescending ? 'desc' : 'asc', 1);
      } else {
        // Change segment sort direction (and add it to sort segments list if not already there)
        // if shift is pressed add segment to existing ones. if not, set this column as
        // the only segment of sort
        const ordrIdx = column.orderIndex;
        // eslint-disable-next-line no-nested-ternary
        const oSeq = event.shiftKey ? (ordrIdx === 0 ? this.numSortedCols + 1 : ordrIdx) : 1;
        // eslint-disable-next-line no-nested-ternary
        const oDir = event.shiftKey ? (this.column.isAscending ? 'desc' : 'asc') : column.cycleOrdering;
        this.$parent.$parent.changeOrder(colIdx, oDir, oSeq, !event.shiftKey);
      }
    },
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
