<template>
  <svg v-if="ordering.isOrderable" :key="ordering.changeCounter" viewBox="0 -5 100 110" width="1em" height="1.1em">
    <g stroke="currentColor" fill="currentColor" stroke-width="4">
      <g v-if="showSegmentNo()">
        <path v-if="showArrowUp()" d="M10 35 A45 30 0 0 1 90 35L 50 -5, 10 35"/>
        <ellipse cx="50" :cy="numberPos()" rx="45" ry="30" fill="none" stroke-width="7"/>
        <text x="50" :y="numberPos() + 5" style="font: 45px sans-serif" dominant-baseline="middle" text-anchor="middle">
          {{ ordering.segment }}
        </text>
        <path v-if="showArrowDown()" d="M10 65 A45 30 0 0 0 90 65L 50 105, 10 65"/>
      </g>
      <g v-else>
        <path d="M25 35 A45 30 0 0 1 75 35L 50 -5, 25 35"/>
        <path d="M25 65 A45 30 0 0 0 75 65L 50 105, 25 65"/>
      </g>
    </g>
  </svg>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import ColumnOrdering from './definitions/column-ordering';
import OrderingDirection from './definitions/column-ordering-direction';

export default /* #__PURE__ */ defineComponent({
  name: 'OrderingIndicator',
  props: { ordering: { type: ColumnOrdering, required: true } },
  methods: {
    numberPos() { return this.ordering.direction === OrderingDirection.ASC ? 65 : 35; },
    showArrowUp() { return !this.ordering.isOrdered || this.ordering.direction !== OrderingDirection.DESC; },
    showArrowDown() { return !this.ordering.isOrdered || this.ordering.direction !== OrderingDirection.ASC; },
    showSegmentNo() { return this.ordering.isOrdered && this.ordering.direction !== OrderingDirection.UNORDERED; },
  },
});
</script>
