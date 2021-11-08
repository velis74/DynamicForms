<template>
  <div v-if="actions.list.length > 0" class="actions-holder">
    <component
      :is="action.elementType"
      v-for="action in actions.list"
      :key="action.name + action.icon"
      class="btn btn-sm btn-info text-nowrap dynamicforms-actioncontrol button"
      :name="'btn-' + action.name"
      v-bind="action.bindAttrs"
      @click.stop="actions.exec($event, action, row)"
    >
      <IonIcon class="d-inline-block" :name="action.icon"/>
      <span class="d-none d-md-inline-block">{{ action.label }}</span>
    </component>
  </div>
</template>

<script>
import IonIcon from './ionicon.vue';

export default {
  name: 'Actions',
  components: { IonIcon },
  props: {
    row: { type: Object, default: () => null },
    actions: { type: Object, required: true },
  },
};
</script>

<style scoped>
.actions-holder {
  transform: scale(.75, .75);
  display: inline-block;
  margin: -.5em;
}

.actions-holder div:not(:first-child) {
  margin-left: .5em;
}

.actions-holder .btn :not(:first-child) {
  margin-left: .5em;
}
</style>
