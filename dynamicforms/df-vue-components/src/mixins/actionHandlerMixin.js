import _ from 'lodash';
import apiClient from '../apiClient';
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
  methods: {
    executeTableAction(action, data, modal, params) {
      if (!_.size(action)) {
        return;
      }
      if (action.name === 'delete') {
        const url = params && params.detailUrl ? params.detailUrl : this.detail_url.replace('--record_id--', data.id);
        callDbFunction({
          method: 'delete',
          url,
          then: () => {
            if (this && this.processedConfiguration) this.processedConfiguration.rows.deleteRow(data.id);
          },
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

        // noinspection JSUnresolvedVariable
        const url = params && params.detailUrl ? params.detailUrl : this.detail_url.replace('--record_id--', dataId);
        const headers = params && 'headers' in params ?
          params.headers : { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1, 'x-df-component-def': true };

        callDbFunction({
          method: submitMethod,
          url,
          data,
          config: { headers },
          then: (res) => {
            if (modal) modal.hide();
            if (this && this.processedConfiguration) this.processedConfiguration.rows.updateRows([res.data]);
          },
          catch: (reason) => {
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
          },
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
