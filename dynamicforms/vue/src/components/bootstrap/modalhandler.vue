<template>
  <div :id="uuid" :class="'modal fade ' + className" tabindex="-1" role="dialog" aria-hidden="true">
    <div :class="'modal-dialog ' + sizeClass" role="document">
      <div class="modal-content">
        <div :class="'modal-header ' + headerClasses">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <transition name="flip" mode="out-in">
          <div v-if="isComponent" :key="uniqId" class="modal-body">
            <div :is="body.component" v-bind="body"/>
          </div>
          <div v-else :key="uniqId" class="modal-body" v-html="body"/>
        </transition>
        <div class="modal-footer">
          <button
            v-for="button in buttons"
            :id="button.element_id || button.uuid"
            :key="button.uuid"
            type="button"
            :class="button.classes"
            v-bind="button.arias"
            @click.stop="buttonClick($event, button, callback)"
          >
            {{ button.label }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import 'bootstrap';
import * as $ from 'jquery';

import apiClient from '../../apiClient';
import DynamicForms from '../../dynamicforms';
import eventBus from '../../logic/eventBus';

import DFFormLayout from './form/dfformlayout.vue';
import DFLoadingIndicator from './loadingindicator.vue';

export default {
  name: 'ModalHandler',
  components: {
    DFFormLayout, DFLoadingIndicator,
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
    if (!DynamicForms.dialog) {
      DynamicForms.dialog = this;
      window.setInterval(() => { this.progressDialogCheck(); }, 250);
    }
  },
  methods: {
    show: function show(dialogDef) {
      if (dialogDef !== undefined) {
        this.dialogs.push(dialogDef);
        const promise = {};
        promise.promise = new Promise((resolve, reject) => {
          promise.resolve = resolve;
          promise.reject = reject;
        });
        dialogDef.promise = promise;
      }
      if (!this.initialEventAssignDone) {
        // created is too soon. if we try to do this there, the dialog won't even show.
        this.initialEventAssignDone = true;
        $(this.bootstrapDialog).on('hide.bs.modal', (event) => {
          let callback = null;
          if (this.dialogs.length) {
            const closedDialog = this.dialogs.pop();
            callback = closedDialog.callback;
            // this default promise resolution  offers no values. We'd probably like to know which button closed?
            // or even what data there was in the dialog? So we're counting on tableActionExecuted event listeners
            // to resolve the promise first with more detailed data.
            // This resolution will then be moot https://stackoverflow.com/a/29491617/1760858
            if (closedDialog.promise) {
              closedDialog.promise.resolve(
                closedDialog.promise.resolveData || `dialog "${closedDialog.title}" closed`,
              );
            }
          }
          if (this.dialogs.length) event.preventDefault();
          if (callback && callback.df_called !== true) callback(null);
        });
      }
      $(this.bootstrapDialog).modal('show');
      return this.currentDialog.promise?.promise; // should return the promise object of last inserted dialog
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
        promise: this.currentDialog.promise,
      });
      if (callback) {
        callback(button.data_return);
        callback.df_called = true;
      }
    },
    message(title, message, callback) {
      return this.show({
        title, body: message, buttons: [{ close: 'default' }], callback,
      });
    },
    yesNo(title, question, callback) {
      return this.show({
        title, body: question, buttons: [{ yes: 'default' }, { no: 'default' }], callback,
      });
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
      return this.show({
        title,
        body: {
          component: 'DFLoadingIndicator', loading: true, label: null, progress: null, data: true,
        },
        buttons: [],
        callback: null,
        isProgress: true,
      });
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
    async showComponent(componentDef, whichTitle, tableUuid) {
      const cDef = componentDef.data;
      const actions = cDef.dialog.actions;

      return this.show({
        uuid: cDef.uuid,
        title: cDef.titles[whichTitle || 'new'],
        body: {
          uuid: cDef.uuid,
          rows: cDef.dialog.rows,
          record: cDef.record,
          component: cDef.dialog.component_name,
        },
        buttons: Object.keys(actions).reduce(
          (res, key) => {
            actions[key].data_return = { dialog_id: cDef.uuid, button: actions[key] };
            res.push(actions[key]);
            return res;
          }, [],
        ),
        callback: null,
        size: cDef.dialog.size,
        header_classes: cDef.dialog.header_classes,
        tableUuid,
        promise: componentDef.promise,
      });
    },
    async fromURL(url, whichTitle, tableUuid) {
      try {
        const res = await apiClient.get(url, { headers: { 'x-viewmode': 'FORM' } });
        // set component is re-rendered
        eventBus.$emit('showingRESTForm', { tableUUID: tableUuid, formUUID: res.data.uuid });
        return this.showComponent({ component: 'DFFormLayout', data: res.data }, whichTitle, tableUuid);
      } catch (err) {
        console.error(err);
        throw err;
      }
    },
  },
};
</script>

<style scoped>

</style>
