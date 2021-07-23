<template>
  <div class="modal fade" id="df-modal-handler" tabindex="-1" role="dialog" aria-hidden="true">
    <div :class="'modal-dialog ' + sizeClass" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <transition name="flip" mode="out-in">
          <div class="modal-body" v-if="isComponent" :key="uniqId">
            <div :is="body.component.replace(/-/g, '')" :data="body.data"/>
          </div>
          <div class="modal-body" v-else :key="uniqId" v-html="body"/>
        </transition>
        <div class="modal-footer">
          <button :id="button.uuid" type="button" v-for="button in buttons" :key="button.uuid"
                  :class="button.classes" v-bind="button.arias"
                  @click.stop="buttonClick(button, callback)">{{ button.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import apiClient from '@/apiClient';
import dfformlayout from '@/components/bootstrap/form/dfformlayout.vue';
import * as $ from 'jquery';
import 'bootstrap';

export default {
  name: 'modalhandler',
  data() {
    return {
      dialogs: [],
      initialEventAssignDone: false, // unfortunately, created() is too soon to attach
      // event listener to the dialog
      uniqIdCounter: 0, // only for giving a truly unique key to dialogs so that we can
      // do proper reactivity
      loading: false, // loading dialog. show progress indicator
    };
  },
  computed: {
    bootstrapDialog() {
      return '#df-modal-handler';
    },
    currentDialog() {
      const res = this.dialogs.length ? this.dialogs[this.dialogs.length - 1] : null;
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      if (res) res.uniqId = res.uniqId || this.uniqIdCounter++;
      return res;
    },
    sizeClass() {
      const dlg = this.currentDialog;
      if (!dlg) return 'modal-sm';
      if (dlg.large || ['large', 'lg', 'modal-lg'].includes(dlg.size)) return 'modal-lg';
      if (dlg.small || ['small', 'sm', 'modal-sm'].includes(dlg.size)) return 'modal-sm';
      return '';
    },
    title() {
      return this.currentDialog ? this.currentDialog.title : 'No dialogs to show!';
    },
    body() {
      return this.currentDialog ? this.currentDialog.body : 'No dialogs have been invoked';
    },
    callback() {
      return this.currentDialog ? this.currentDialog.callback : null;
    },
    uniqId() {
      return this.currentDialog ? this.currentDialog.uniqId : null;
    },
    isComponent() {
      return this.currentDialog ? this.currentDialog.body.component
          && this.currentDialog.body.data : false;
    },
    buttons() {
      const cdb = this.currentDialog ? this.currentDialog.buttons : null;
      const res = this.currentDialog && cdb ? cdb : [{ close: 'default' }];
      return res.map((value) => {
        if (value.close === 'default') {
          // eslint-disable-next-line no-param-reassign
          value = {
            label: this.gettext('Close'),
            classes: 'btn btn-secondary',
            data_return: 'close',
          };
        } else if (value.yes === 'default') {
          // eslint-disable-next-line no-param-reassign
          value = {
            label: this.gettext('Yes'),
            classes: 'btn btn-primary',
            data_return: 'yes',
          };
        } else if (value.no === 'default') {
          // eslint-disable-next-line no-param-reassign
          value = {
            label: this.gettext('No'),
            classes: 'btn btn-secondary',
            data_return: 'no',
          };
        }
        value.arias = value.arias || {};
        value.guid = value.guid || '';
        const clss = (value.classes || '').split(' ');
        if (clss.indexOf('btn') === -1) clss.push('btn');
        value.classes = clss.join(' ');
        return value;
      });
    },
  },
  created() {
    // make our API available
    if (!window.dynamicforms.dialog) {
      window.dynamicforms.dialog = this;
    }
  },
  methods: {
    show: function show() {
      if (!this.initialEventAssignDone) {
        // created is too soon. if we try to do this there, the dialog won't even show.
        this.initialEventAssignDone = true;
        $(this.bootstrapDialog).on('hide.bs.modal', (event) => {
          let callback = null;
          if (this.dialogs.length) callback = this.dialogs.pop().callback;
          if (this.dialogs.length) event.preventDefault();
          if (callback && callback.df_called !== true) callback(null);
        });
      }
      $(this.bootstrapDialog).modal('show');
    },
    hide: function hide() {
      $(this.bootstrapDialog).modal('hide');
    },
    // gettext: (str) => window.django.gettext(str),
    gettext: (str) => str,
    buttonClick(button, callback) {
      if (callback) {
        callback(button.data_return);
        callback.df_called = true;
      }
      this.hide();
    },
    yesNo(title, question, callback) {
      this.dialogs.push({
        title, body: question, buttons: [{ yes: 'default' }, { no: 'default' }], callback,
      });
      this.show();
    },
    showComponent(componentDef, whichTitle) {
      const actions = componentDef.data.dialog.actions;
      this.dialogs.push({
        title: componentDef.data.titles[whichTitle || 'new'],
        body: componentDef,
        buttons: Object.keys(actions).reduce(
          (res, key) => {
            actions[key].data_return = { dialog_id: componentDef.data.uuid, button: actions[key] };
            res.push(actions[key]);
            return res;
          }, [],
        ),
        callback: null,
      });
      this.show();
    },
    fromURL(url, whichTitle) {
      this.loading = true;
      apiClient.get(url, { headers: { 'x-viewmode': 'FORM', 'x-df-render-type': 'dialog' } })
          .then((res) => { // call api and set data as response, when data is
            // set component is re-rendered
            this.showComponent(res.data, whichTitle);
          }).catch((err) => {
            console.error(err);
          }).finally(() => {
            this.loading = false;
          });
    },
  },
  components: {
    dfformlayout,
  },
};
</script>

<style scoped>

</style>
