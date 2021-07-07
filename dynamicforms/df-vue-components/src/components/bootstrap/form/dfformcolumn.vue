<template>
  <div class="col" v-if="isGroup">
    <div class="card">
      <div class="card-header">
        {{ def.title }}
      </div>
      <div class="card-body">
        <component :is="def.field.render_params.form.replace(/-/g, '')"
                   :def="def.field" :data="data"/>
      </div>
      <div class="card-footer" v-if="def.footer">
        {{ def.footer }}
      </div>
    </div>
  </div>
  <component v-else-if="isHidden"
             :is="def.field.render_params.form.replace(/-/g, '')"
             :def="def.field" :data="data"/>
  <div :class="'col' + columnClasses" v-else>
    <component :is="def.field.render_params.form.replace(/-/g, '')"
               :def="def.field" :data="data"/>
  </div>
</template>

<script>
import DisplayMode from '@/logic/displayMode';
import dfwidgetinput from '@/components/bootstrap/widget/dfwidgetinput.vue';
import dfwidgetpassword from '@/components/bootstrap/widget/dfwidgetpassword.vue';

export default {
  name: 'dfformcolumn',
  props: ['def', 'data'],
  created() {
    // console.log(this.def, this.data, 5678);
  },
  computed: {
    isGroup() { return this.def.type === 'group'; },
    isHidden() { return this.def.field.display === DisplayMode.HIDDEN; },
    columnClasses() { return this.def.width_classes ? ` ${this.def.width_classes}` : ''; },
  },
  components: {
    dfwidgetinput,
    dfwidgetpassword,
  },
};
</script>

<style scoped>

</style>
