import apiClient from '@/apiClient';
import _ from 'lodash';
import eventBus from '@/logic/eventBus';

const tableActionHandlerMixin = {
  methods: {
    executeTableAction(action, data, modal) {
      if (!_.size(action)) {
        return;
      }
      if (action.name === 'delete') {
        apiClient.delete(this.detail_url.replace('--record_id--', data.id))
          .then(() => {
            this.processedConfiguration.rows.deleteRow(data.id);
          });
      } else if (['edit', 'add'].includes(action.name)) {
        this.showModal(action, data);
      } else if (action.name === 'submit') {
        let dataId;
        let submitMethod;
        if (data.id) {
          dataId = data.id;
          submitMethod = apiClient.put;
        } else {
          dataId = 'new';
          submitMethod = apiClient.post;
        }

        submitMethod(this.detail_url.replace('--record_id--', dataId), data,
          { headers: { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1, 'x-df-component-def': true } })
          .then((res) => {
            if (modal) modal.hide();
            this.processedConfiguration.rows.updateRows([res.data]);
          })
          .catch((reason) => {
            const dfErrors = {};
            const eventName = `formEvents_${modal.currentDialog.body.data.uuid}`;
            if (reason.response.status === 400) {
              _.forOwn(reason.response.data, (value, key) => {
                dfErrors[`${key}`] = _.join(value, '\n');
              });
            } else {
              dfErrors.non_field_errors = reason.response.data.detail;
            }

            eventBus.$emit(eventName, { type: 'submitErrors', data: dfErrors });
          });
      } else if (action.name === 'cancel') {
        if (modal) modal.hide();
      } else if (action.name === 'filter') {
        this.loadData();
      }
    },
  },
};

export default tableActionHandlerMixin;
