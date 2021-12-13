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
  } else params = [payload.url, payload.config];

  apiClient[payload.method].apply(this, params)
    .then((res) => { thenFunction(res); })
    .catch((res) => { catchFunction(res); })
    .finally(() => { finallyFunction(); });
};

const actionHandlerMixin = {
  mounted() {
    eventBus.$on(`tableActionExecuted_${this.uuid}`, this.tableAction);
  },
  beforeDestroy() {
    eventBus.$off(`tableActionExecuted_${this.uuid}`);
  },
  methods: {
    tableAction(payload) {
      if (['add', 'edit', 'delete', 'filter', 'submit', 'cancel'].includes(payload.action.name)) {
        this.executeTableAction(payload.action, payload.data, payload.modal, {});
      } else {
        const action = payload.action ? payload.action.action : null;
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
    },
    executeTableAction(action, data, modal, params) {
      if (!_.size(action)) {
        return;
      }
      if (action.name === 'delete') {
        const url = params && params.detailUrl ? params.detailUrl : this.detail_url.replace('--record_id--', data.id);
        callDbFunction({
          method: 'delete',
          url,
          then: params.then ||
            (() => {
              if (this && this.processedConfiguration) this.processedConfiguration.rows.deleteRow(data.id);
            }),
        });
      } else if (['edit', 'add'].includes(action.name)) {
        this.showModal(action, data);
      } else if (action.name === 'submit') {
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

        // noinspection JSUnresolvedVariable
        const url = params && params.detailUrl ? params.detailUrl : this.detail_url.replace('--record_id--', dataId);
        const headers = params && 'headers' in params ?
          params.headers : { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1, 'x-df-component-def': true };
        const self = this;

        callDbFunction({
          method: submitMethod,
          url,
          data,
          config: { headers },
          then: params.then ||
            ((res) => {
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
      } else if (action.name === 'cancel') {
        if (modal) modal.hide();
      } else if (action.name === 'filter') {
        this.loadData();
      }
    },
  },
};

export default actionHandlerMixin;
