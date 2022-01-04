import _ from 'lodash';

import apiClient from '../apiClient';
import DynamicForms from '../dynamicforms';
import eventBus from '../logic/eventBus';

const callDbFunction = (payload) => {
  const thenFunction = (res) => {
    if (payload.then) payload.then(res);
  };

  const catchFunction = (res) => {
    if (payload.catch) payload.catch(res);
  };

  const finallyFunction = () => {
    if (payload.finally) payload.finally();
  };

  let params;
  if (['put', 'post', 'patch'].includes(payload.method)) {
    params = [payload.url, payload.data, payload.config];
  } else {
    params = [payload.url, payload.config];
  }

  apiClient[payload.method].apply(this, params)
    .then((res) => { thenFunction(res); })
    .catch((res) => { catchFunction(res); })
    .finally(() => { finallyFunction(); });
};

const actionHandlerMixin = {
  /*
   * Expects the master object to have the following properties and methods:
   * - uuid: string  (all actions)
   * - showModal(action, data)   (add and edit)
   * - detail_url: string with --record_id--  (delete and submit)
   * - processedConfiguration: object (optional for delete and submit methods)
   * - loadData() (optional for filter method)
   * - defaultSubmitHeaders() calculated value specifying custom headers for submit button
   */
  computed: {
    defaultSubmitHeaders() { return { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1, 'x-df-component-def': true }; },
  },
  mounted() {
    eventBus.$on(`tableActionExecuted_${this.uuid}`, this.tableAction);
  },
  beforeDestroy() {
    eventBus.$off(`tableActionExecuted_${this.uuid}`);
  },
  methods: {
    tableAction(payload) {
      if (payload.action === undefined || !_.size(payload.action)) return;
      const action = payload.action ? payload.action.action : null;
      const actionName = payload.action.name;
      const actionNameTitleCase = actionName.charAt(0).toUpperCase() + actionName.slice(1);
      const actionMethodName = `action${actionNameTitleCase}Execute`;
      const actionMethod = this[actionMethodName] instanceof Function ? this[actionMethodName] : null;

      switch (actionName) {
      case 'add':
        this.actionAddExecute(payload.action, payload.data, payload.modal, {}, payload.promise);
        break;
      case 'edit':
        this.actionEditExecute(payload.action, payload.data, payload.modal, {}, payload.promise);
        break;
      case 'delete':
        this.actionDeleteExecute(payload.action, payload.data, payload.modal, {}, payload.promise);
        break;
      case 'filter':
        this.actionFilterExecute(payload.action, payload.data, payload.modal, {}, payload.promise);
        break;
      case 'submit':
        this.actionSubmitExecute(payload.action, payload.data, payload.modal, {}, payload.promise);
        break;
      case 'cancel':
        this.actionCancelExecute(payload.action, payload.data, payload.modal, {}, payload.promise);
        break;
      default:
        if (actionMethod != null) {
          // So the method for this action has been implemented elsewhere, and now we will call it
          actionMethod.apply(this, [payload.action, payload.data, payload.modal, {}, payload.promise]);
        } else {
          if (action === null) return; // Action is empty or not there, nothing will be executed

          if (action.href) {
            // action is a link to a subpage or to a router path
            // we will do nothing because the action was already rendered as a link
          } else {
            // Action is a call to a function with some parameters
            const func = DynamicForms.getObjectFromPath(payload.action.action.func_name);
            if (func) {
              let params = {};
              try {
                params = payload.action.action.params;
                // eslint-disable-next-line no-empty
              } catch (e) {}
              const data = { context: this, ...payload };
              if (params) {
                func.apply(params, [data]);
              } else {
                func(data);
              }
            }
          }
        }
      }
    },
    actionAddExecute(action, data, modal, params, promise) { // eslint-disable-line no-unused-vars
      this.showModal(action, data);
    },
    actionEditExecute(action, data, modal, params, promise) { // eslint-disable-line no-unused-vars
      this.showModal(action, data);
    },
    actionDeleteExecute(action, data, modal, params, promise) { // eslint-disable-line no-unused-vars
      const url = params && params.detailUrl ? params.detailUrl : this.detail_url.replace('--record_id--', data.id);
      callDbFunction({
        method: 'delete',
        url,
        then: params.then ||
          (() => {
            if (this && this.processedConfiguration) this.processedConfiguration.rows.deleteRow(data.id);
          }),
      });
    },
    actionSubmitExecute(action, data, modal, params, promise) {
      let dataId;
      let submitMethod;
      if (data.id) {
        dataId = data.id;
        submitMethod = 'put';
      } else {
        dataId = 'new';
        submitMethod = 'post';
      }
      submitMethod = params.submitMethod || submitMethod;

      if (promise) promise.resolveData = { action, data, params };

      // noinspection JSUnresolvedVariable
      const url = params && params.detailUrl ? params.detailUrl : this.detail_url.replace('--record_id--', dataId);
      const headers = (params ? params.headers : null) || this.defaultSubmitHeaders;
      const self = this;

      callDbFunction({
        method: submitMethod,
        url,
        data,
        config: { headers },
        then: params.then ||
          ((res) => {
            // update resolve data with record that came back from the server
            if (promise) promise.resolveData = { action, data: res.data, params };
            if (modal) modal.hide();
            if (self && self.processedConfiguration) self.processedConfiguration.rows.updateRowFromForm(res.data);
          }),
        catch: params.catch ||
          ((reason) => {
            const dfErrors = {};
            const eventName = `formEvents_${modal.currentDialog.body.uuid}`;
            if (reason.response.status === 400) {
              _.forOwn(reason.response.data, (value, key) => {
                dfErrors[`${key}`] = _.join(value, '\n');
              });
            } else {
              dfErrors.non_field_errors = reason.response.data.detail;
            }

            eventBus.$emit(eventName, { type: 'submitErrors', data: dfErrors });
          }),
      });
    },
    actionCancelExecute(action, data, modal, params, promise) {
      if (promise) promise.resolveData = { action, data, params };
      if (modal) modal.hide();
    },
    actionFilterExecute(action, data, modal, params, promise) { // eslint-disable-line no-unused-vars
      this.loadData();
    },
  },
};

export default actionHandlerMixin;
