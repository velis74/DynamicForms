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

import apiClient from '../../apiClient';
import DynamicForms from '../../dynamicforms';
import translationsMixin from '../../mixins/translationsMixin';

import DFFormLayout from './form/dfformlayout.vue';
import DFLoadingIndicator from './loadingindicator.vue';

export default {
  name: 'ModalHandler',
  components: {
    DFFormLayout, DFLoadingIndicator,
  },
  mixins: [translationsMixin],
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
    isShowingProgress() { return this.currentDialog && this.currentDialog.isProgress === true; },
  },
  created() {
    // make our API available
    if (!DynamicForms.dialog) {
      DynamicForms.dialog = this;
      window.setInterval(() => { this.progressDialogCheck(); }, 250);
    }
  },
  methods: {
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
  },
};
</script>

<style scoped>

</style>
