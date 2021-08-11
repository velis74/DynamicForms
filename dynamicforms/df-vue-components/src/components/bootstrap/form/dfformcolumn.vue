<template>
  <div class="col" v-if="isGroup">
    <div class="card">
      <div class="card-header">
        {{ def.title }}
      </div>
      <div class="card-body">
        <component :is="def.field.render_params.form.replace(/-/g, '')"
                   :def="def.field" :data="data" :errors="errors"/>
      </div>
      <div class="card-footer" v-if="def.footer">
        {{ def.footer }}
      </div>
    </div>
  </div>
  <component v-else-if="isHidden"
             :is="def.field.render_params.form.replace(/-/g, '')"
             :def="def.field" :data="data" :errors="errors"/>
  <div :class="'col' + columnClasses" v-else>
    <component :is="def.field.render_params.form.replace(/-/g, '')"
               :def="def.field" :data="data" :errors="errors"/>
  </div>
</template>

<style>
  label {
    margin-inline-end: .5em;
  }
</style>

<script>
import DisplayMode from '@/logic/displayMode';
import dfwidgetinput from '@/components/bootstrap/widget/dfwidgetinput.vue';
import dfwidgetpassword from '@/components/bootstrap/widget/dfwidgetpassword.vue';
import dfwidgetckeditor from '@/components/bootstrap/widget/dfwidgetckeditor.vue';
import dfwidgetselect from '@/components/bootstrap/widget/dfwidgetselect.vue';

export default {
  name: 'dfformcolumn',
  props: ['def', 'data', 'errors'],
  computed: {
    isGroup() { return this.def.type === 'group'; },
    isHidden() {
      return this.def.field.visibility.form === DisplayMode.HIDDEN;
    },
    columnClasses() { return this.def.width_classes ? ` ${this.def.width_classes}` : ''; },
  },
  components: {
    dfwidgetinput,
    dfwidgetpassword,
    dfwidgetckeditor,
    dfwidgetselect,
  },
};
</script>

<style scoped>

</style>
