<template>
  <div :class="'modal fade ' + className" :id="uuid" tabindex="-1" role="dialog" aria-hidden="true">
    <div :class="'modal-dialog ' + sizeClass" role="document">
      <div class="modal-content">
        <div :class="'modal-header ' + headerClasses">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <transition name="flip" mode="out-in">
          <div class="modal-body" v-if="isComponent" :key="uniqId">
            <div :is="body.component" v-bind="body"/>
          </div>
          <div class="modal-body" v-else :key="uniqId" v-html="body"/>
        </transition>
        <div class="modal-footer">
          <button :id="button.element_id || button.uuid" type="button" v-for="button in buttons" :key="button.uuid"
                  :class="button.classes" v-bind="button.arias"
                  @click.stop="buttonClick($event, button, callback)">{{ button.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import * as $ from 'jquery';
import apiClient from '../../apiClient';
import dfformlayout from './form/dfformlayout.vue';
import dfloadingindicator from './loadingindicator.vue';
import 'bootstrap';
import eventBus from '../../logic/eventBus';
import dynamicforms from '../../dynamicforms';

export default {
  name: 'modalhandler',
  components: {
    dfformlayout, dfloadingindicator,
  },
  data() {
    return {
      dialogs: [],
      // initialEventAssignDone: unfortunately, created() is too soon to attach event listener to the dialog, so we
      // attach the onclose event handler upon first dialog show
      initialEventAssignDone: false,
      // uniqIdCounter: only for giving a truly unique key to dialogs so that we can do proper reactivity
      uniqIdCounter: 0,
      inFlightRequests: {}, // we track currently active requests this way
    };
  },
  computed: {
    className() { return 'df-modal-handler'; },
    bootstrapDialog() {
      return '.df-modal-handler';
    },
    currentDialog() {
      const res = this.dialogs.length ? this.dialogs[this.dialogs.length - 1] : null;
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      if (res) res.uniqId = res.uniqId || this.uniqIdCounter++;
      return res; // type: Object
    },
    sizeClass() {
      const dlg = this.currentDialog;
      if (!dlg) return 'modal-sm';
      if (dlg.large || ['large', 'lg', 'modal-lg'].includes(dlg.size)) return 'modal-lg';
      if (dlg.small || ['small', 'sm', 'modal-sm'].includes(dlg.size)) return 'modal-sm';
      return '';
    },
    headerClasses() {
      const dlg = this.currentDialog;
      if (!dlg) return '';
      return dlg.header_classes || '';
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
      return Boolean(this.currentDialog && this.currentDialog.body && this.currentDialog.body.component);
    },
    uuid() {
      return this.currentDialog && this.currentDialog.uuid ? `dialog-${this.currentDialog.uuid}` : 'df-modal-handler';
    },
    isShowingProgress() { return this.currentDialog && this.currentDialog.isProgress === true; },
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
        const clss = (value.classes || '').split(' ');
        if (clss.indexOf('btn') === -1) clss.push('btn');
        value.classes = clss.join(' ');
        return value;
      });
    },
  },
  created() {
    // make our API available
    if (!dynamicforms.dialog) {
      dynamicforms.dialog = this;
      window.setInterval(() => { this.progressDialogCheck(); }, 250);
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
    buttonClick(event, button, callback) {
      eventBus.$emit(`tableActionExecuted_${this.currentDialog.tableUuid}`, {
        action: button,
        data: this.currentDialog.body.record,
        modal: this,
        event,
      });
      if (callback) {
        callback(button.data_return);
        callback.df_called = true;
      }
    },
    message(title, message, callback) {
      this.dialogs.push({
        title, body: message, buttons: [{ close: 'default' }], callback,
      });
      this.show();
    },
    yesNo(title, question, callback) {
      this.dialogs.push({
        title, body: question, buttons: [{ yes: 'default' }, { no: 'default' }], callback,
      });
      this.show();
    },
    loading() { return Object.keys(this.inFlightRequests).length; },
    oldestInFlight() {
      /**
       * Reports the oldest active request's properties. All properties are null if there is no active request.
       */
      const inFlightReq = this.inFlightRequests;
      const inFlightKeys = Object.keys(inFlightReq);
      if (inFlightKeys.length === 0) return { requestId: null, timestamp: null, age: null };
      return {
        requestId: inFlightKeys[0],
        timestamp: inFlightReq[inFlightKeys[0]],
        age: new Date().getTime() - inFlightReq[inFlightKeys[0]],
      };
    },
    progressDialogCheck() {
      /**
       * checks if there are any ongoing requests that are running for 250ms or more. If that's the case, show progress
       */
      if (this.oldestInFlight().age >= 250 && !this.isShowingProgress) {
        this.showProgress();
      } else if (this.oldestInFlight().age >= 250 && this.isShowingProgress) {
        apiClient.get('/dynamicforms/progress/',
          { headers: { 'x-df-timestamp': this.oldestInFlight().timestamp } })
          .then((res) => { // call api and set data as response, when data is
            // we need to recheck because after the request, the dialog might no longer show
            if (this.isShowingProgress) {
              this.currentDialog.body.progress = Number(res.data.value);
              this.currentDialog.body.label = res.data.comment;
            }
          })
          .catch((err) => { console.error(err); });
      } else if (this.loading() === 0 && this.isShowingProgress) {
        this.hide();
      }
    },
    showProgress() {
      console.log(
        `Showing progress: We have ${this.loading()} active requests to server oldest is ` +
        `${this.oldestInFlight().age}ms old with timestamp ${this.oldestInFlight().timestamp}.`,
      );
      const title = 'Performing operation';
      this.dialogs.push({
        title,
        body: {
          component: 'dfloadingindicator', loading: true, label: null, progress: null, data: true,
        },
        buttons: [],
        callback: null,
        isProgress: true,
      });
      this.show();
    },
    addRequest(requestId) {
      /**
       * Adds a new active request to track. If the request does not complete in 250ms, progress dialog will be shown
       */
      this.inFlightRequests[requestId] = new Date().getTime();
      return { sequence: requestId, timestamp: this.inFlightRequests[requestId] };
    },
    removeRequest(requestId) {
      /**
       * Removes (no longer) active request from tracking. Any open progress dialogs will be hidden
       */
      if (!requestId) return; // this will be true for progress requests made by progressDialogCheck function
      delete this.inFlightRequests[requestId];
      this.progressDialogCheck(); // first we remove the progress dialog when all requests are done
    },
    showComponent(componentDef, whichTitle, tableUuid) {
      const actions = componentDef.data.dialog.actions;
      this.dialogs.push({
        uuid: componentDef.data.uuid,
        title: componentDef.data.titles[whichTitle || 'new'],
        body: {
          uuid: componentDef.data.uuid,
          rows: componentDef.data.dialog.rows,
          record: componentDef.data.record,
          component: componentDef.data.dialog.component_name,
        },
        buttons: Object.keys(actions).reduce(
          (res, key) => {
            actions[key].data_return = { dialog_id: componentDef.data.uuid, button: actions[key] };
            res.push(actions[key]);
            return res;
          }, [],
        ),
        callback: null,
        size: componentDef.data.dialog.size,
        header_classes: componentDef.data.dialog.header_classes,
        tableUuid,
      });
      this.show();
    },
    fromURL(url, whichTitle, tableUuid) {
      apiClient.get(url, { headers: { 'x-viewmode': 'FORM', 'x-df-render-type': 'dialog' } })
        .then((res) => { // call api and set data as response, when data is
          // set component is re-rendered
          this.showComponent(res.data, whichTitle, tableUuid);
        })
        .catch((err) => { console.error(err); });
    },
  },
};
</script>

<style scoped>

</style>
