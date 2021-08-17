<template>
  <div>
    <component :is="component + 'table'" v-on:setTableFilter="setTableFilter"
               :configuration="processedConfiguration"></component>
  </div>
</template>

<script>
import bootstraptable from '@/components/bootstrap/table/dftable.vue';
// import JqueryuiTable from '@/components/jqueryui/Table.vue';
import ActionsHandler from '@/logic/actionsHandler';
import TableColumn from '@/logic/tableColumn';
import apiClient from '@/apiClient';
import _ from 'lodash';
import $ from 'jquery';
import DisplayMode from '@/logic/displayMode';
import tableActionHandlerMixin from '@/mixins/tableActionHandlerMixin';
import eventBus from '@/logic/eventBus';
import dynamicforms from '@/dynamicforms';

export default {
  name: 'dftable',
  mixins: [tableActionHandlerMixin],
  props: {
    config: { type: Object, required: false },
  },
  data() {
    const cfg = this.config || this.$parent;
    return {
      loading: false,
      rows: cfg.rows,
      columns: _.filter(cfg.columns, (c) => DisplayMode.FULL === c.visibility.table),
      titles: cfg.titles,
      actions: cfg.actions,
      uuid: cfg.uuid,
      list_url: cfg.list_url,
      detail_url: cfg.detail_url,
      editingRowURL: cfg.editingRowURL,
      editDialogTitle: cfg.editDialogTitle,
      filter: cfg.filter,
      filterQueryString: '',
    };
  },
  beforeDestroy() {
    eventBus.$off(`tableActionExecuted_${this.uuid}`);
  },
  mounted() {
    let bodyColumnCss = '';
    this.columns.forEach((column, idx) => {
      bodyColumnCss += `#list-${this.uuid} tbody tr td:nth-child(${idx + 1}) {
            text-align: ${column.alignment};
          }
          `;
    });
    const styleTag = document.createElement('style');
    styleTag.appendChild(document.createTextNode(bodyColumnCss));
    document.head.appendChild(styleTag);
    eventBus.$on(`tableActionExecuted_${this.uuid}`, this.tableAction);
  },
  computed: {
    processedConfiguration() {
      return {
        rows: this.loadableRows(this.rows),
        columns: this.columns.map((c) => new TableColumn(c)),
        actions: new ActionsHandler(this.actions, this.showModal, this.uuid),
        loading: this.loading,
        noDataString: 'No data',
        editDialogTitle: 'Test dialog',
        editingRowURL: '',
        titles: this.titles,
        filter: this.filter,
      };
    },
    component() {
      return window.dynamicformsUi;
    },
    sortedColumns() {
      return this.processedConfiguration.columns.filter((col) => col.isOrdered && !col.isUnsorted)
        .map((col) => ({ fieldName: col.name, direction: col.isAscending, index: col.orderIndex }))
        .sort((a, b) => a.index - b.index);
    },
    orderingParam() {
      return this.sortedColumns.map((o) => (o.direction === true ? '' : '-') + o.fieldName);
    },
  },
  methods: {
    changeOrder(colIdx, sortDirection, sortSeq, clearAllOthers) {
      const orderChanged = this.processedConfiguration.columns[colIdx].orderIndex !== sortSeq;
      this.processedConfiguration.columns.forEach((column, index) => {
        if (index === colIdx) {
          column.setSorted(sortDirection, sortSeq);
        } else if (column.orderIndex > 0) {
          if (clearAllOthers) {
            column.setSorted('unsorted');
          } else if (orderChanged && column.orderIndex >= sortSeq) {
            column.setSorted(column.isAscending ? 'asc' : 'desc', column.orderIndex + 1);
          }
        }
      });
    },
    loadData() {
      this.loading = true;
      window.setTimeout(() => {
        // if it takes more than 250ms to load the new records, clear existing ones.
        // don't do it before to reduce flicker
        // if (this.loading) this.rows = []; // clear
        // existing rows,
        // we're making a full refresh
      }, 250);
      let url = `${this.list_url}?ordering=${this.orderingParam}`;
      if (_.size(this.filterQueryString)) {
        url += `&${this.filterQueryString}`;
      }
      apiClient.get(url, {
        headers: {
          'x-viewmode': 'TABLE_ROW',
          'x-pagination': 1,
        },
      }).then((res) => {
        // call api and set data as response, when data is set component is re-rendered
        this.rows = res.data;
        // this.rows = this.loadableRows(res.data);
      }).catch((err) => {
        console.error(err);
      }).finally(() => {
        this.loading = false;
      });
    },
    loadableRows(rowsData) {
      let res = [];
      let next = null;
      if (rowsData && rowsData.results && rowsData.results.constructor === Array) {
        res = rowsData.results;
        next = rowsData.next;
      }
      const decorate = (rows) => {
        let triggerRow1 = null;
        let triggerRow2 = null;
        if (rows && rows.length) {
          triggerRow1 = rows[0].id;
          triggerRow2 = rows[rows.length - 1].id;
        }
        res.getVisibilityHandler = (rowId) => (triggerRow1 === rowId || triggerRow2 === rowId ? {
          callback: res.loadMoreRows, once: true,
        } : false);
      };
      decorate(res.length && next ? res : null);
      res.loadMoreRows = (isVisible) => {
        if (!isVisible) return;
        this.loading = true;
        apiClient.get(this.rows.next, {
          headers: {
            'x-viewmode': 'TABLE_ROW',
            'x-pagination': 1,
          },
          // eslint-disable-next-line no-shadow
        }).then((res) => {
          // first we map existing row ids to respective array indexes
          const idIndices = this.rows.results.reduce((ind, item, idx) => {
            ind[item.id] = idx;
            return ind;
          }, {});
          // eslint-disable-next-line array-callback-return
          res.data.results.map((item) => {
            // then we iterate through results updating any existing entries and adding new ones
            const idIdx = idIndices[item.id];
            if (idIdx) {
              this.rows.results[idIdx] = item;
            } else {
              this.rows.results.push(item);
            }
          });
          this.rows.next = res.data.next; // replace next so we can load another set of rows
          // finally create a new loadableRows so that it will load new
          // rows based on this result set
          decorate(res.data.results.length && res.data.next ? res.data.results : null);
        }).catch((err) => {
          console.log(err);
        }).finally(() => { this.loading = false; });
      };
      return res;
    },
    showModal(action, row) {
      if (action.name === 'edit') {
        this.editDialogTitle = `${this.titles.edit} ${row.id}`;
        this.editingRowURL = this.detail_url.replace('--record_id--', row.id).replace('.json', '.component');
        window.dynamicforms.dialog.fromURL(this.editingRowURL, action.name, this.uuid);
      } else if (action.name === 'add') {
        this.editDialogTitle = this.titles.add;
        this.editingRowURL = this.detail_url.replace('--record_id--', 'new').replace('.json', '.component');
        window.dynamicforms.dialog.fromURL(this.editingRowURL, null, this.uuid);
      } else {
        this.editDialogTitle = `unknown action ${action.name}... so, a stupid title`;
        this.editingRowURL = '';
      }
    },
    setTableFilter(filter) {
      console.log(filter);
      this.filterQueryString = $.param(_.pickBy(
        _.clone(filter.filter), (v) => (_.isString(v) ? _.size(v) : v !== null && v !== undefined),
      ));
      if (filter.doFilter) {
        this.loadData();
      }
    },
    tableAction(payload) {
      if (['add', 'edit', 'delete', 'filter', 'submit', 'cancel'].includes(payload.action.name)) {
        this.executeTableAction(payload.action, payload.data, payload.modal);
      } else {
        const func = dynamicforms.getObjectFromPath(payload.action.action.func_name);
        if (func) {
          let params = {};
          try {
            params = payload.action.action.params;
            // eslint-disable-next-line no-empty
          } catch (e) {}
          const data = { context: this, ...payload };
          if (params) func.apply(params, [data]);
          else func(data);
        }
      }
    },
  },
  watch: {
    orderingParam(_newVal, _oldVal) {
      if (!_.isEqual(_newVal, _oldVal)) {
        this.loadData();
      }
    },
  },
  components: {
    bootstraptable,
    // JqueryuiTable,
  },
};
</script>

<style scoped>

</style>
