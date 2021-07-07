<template>
  <div class="actions-holder">
    <div v-for="action in actions.list"
         :key="action.name + action.icon" class="btn btn-sm btn-info text-nowrap"
         @click.stop="actions.exec(action, row)">
      <IonIcon class="d-inline-block" :name="action.icon"/>
      <span class="d-none d-md-inline-block">{{ action.label }}</span></div>
  </div>
</template>

<script>
import IonIcon from '@/components/bootstrap/ionicon.vue';

export default {
  name: 'actions',
  props: ['row', 'actions'],
  components: {
    IonIcon,
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
