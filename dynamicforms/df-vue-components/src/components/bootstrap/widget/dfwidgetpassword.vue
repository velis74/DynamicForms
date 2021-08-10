<template>
  <dfwidgetbase :def="def" :data="data" :errors="errors">
    <div slot="input" class="input-group">
      <input :id="def.uuid" :type="passwordFieldType" v-model='password'
             :class="def.render_params.class"
             :name="def.name"
             :aria-describedby="def.help_text ? def.name + '-help' : null"
             :placeholder="def.placeholder" :value="data[def.name]"
             :pattern="def.render_params.pattern">
      <span @click="toggle_password"
            :class="isPassword ? 'password-field' : 'password-field-slash'"
            class="input-group-text"></span>
    </div>
  </dfwidgetbase>
</template>

<script>
import dfwidgetbase from '@/components/bootstrap/widget/dfwidgetbase.vue';

export default {
  name: 'dfwidgetpassword',
  props: ['def', 'data', 'errors'],
  data() {
    return {
      password: '',
      passwordFieldType: 'password',
      isPassword: true,
    };
  },
  methods: {
    toggle_password() {
      this.isPassword = !this.isPassword;
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password';
    },
  },
  components: {
    dfwidgetbase,
  },
};
</script>

<style scoped>

</style>
