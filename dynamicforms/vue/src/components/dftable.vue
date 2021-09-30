<template>
  <div>
    <component :is="component" :key="drawSeq" :configuration="processedConfiguration" @setTableFilter="setTableFilter"/>
  </div>
</template>

<script>
import $ from 'jquery';
import _ from 'lodash';

// import JQueryUITable from './jqueryui/Table.vue';
import apiClient from '../apiClient';
import DynamicForms from '../dynamicforms';
import ActionsHandler from '../logic/actionsHandler';
import DisplayMode from '../logic/displayMode';
import eventBus from '../logic/eventBus';
import LoadableTableRows from '../logic/loadableTableRows';
import TableColumn from '../logic/tableColumn';
import actionHandlerMixin from '../mixins/actionHandlerMixin';

import BootstrapTable from './bootstrap/table/dftable.vue';

export default {
  name: 'DFTable',
  components: {
    BootstrapTable, // JQueryUITable,
  },
  mixins: [actionHandlerMixin],
  props: {
    config: { type: Object, required: true },
  },
  data() {
    const cfg = this.config || this.$parent;
    return {
      drawSeq: 0,
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
      ordering_parameter: cfg.ordering_parameter,
      ordering_style: cfg.ordering_style,
    };
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
        tableLabel: this.titles.table,
        filter: this.filter,
      };
    },
    component() {
      return `${DynamicForms.UI}Table`;
    },
    sortedColumns() {
      return this.processedConfiguration.columns.filter((col) => col.isOrdered && !col.isUnsorted)
        .map((col) => ({ fieldName: col.name, direction: col.isAscending, index: col.orderIndex }))
        .sort((a, b) => a.index - b.index);
    },
    orderingParam() {
      const orderingStyle = DynamicForms.getObjectFromPath(this.ordering_style);
      if (orderingStyle) {
        return orderingStyle(this.sortedColumns);
      }
      return this.sortedColumns.map((o) => (o.direction === true ? '' : '-') + o.fieldName);
    },
  },
  watch: {
    orderingParam(_newVal, _oldVal) {
      if (!_.isEqual(_newVal, _oldVal)) {
        this.loadData();
      }
    },
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
      // window.setTimeout(() => {
      // if it takes more than 250ms to load the new records, clear existing ones.
      // don't do it before to reduce flicker
      // if (this.loading) this.rows = []; // clear
      // existing rows,
      // we're making a full refresh
      // }, 250);
      let url = `${this.list_url}?${this.ordering_parameter}=${this.orderingParam}`;
      if (_.size(this.filterQueryString)) {
        url += `&${this.filterQueryString}`;
      }
      apiClient.get(url, { headers: { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 } })
        .then((res) => { this.rows = res.data; })
        .catch((err) => { console.error(err); })
        .finally(() => { this.loading = false; });
    },
    loadableRows(rowsData) { return LoadableTableRows(this, rowsData); },
    showModal(action, row) {
      if (action.name === 'edit') {
        this.editDialogTitle = `${this.titles.edit} ${row.id}`;
        this.editingRowURL = this.detail_url.replace('--record_id--', row.id).replace('.json', '.componentdef');
        DynamicForms.dialog.fromURL(this.editingRowURL, action.name, this.uuid);
      } else if (action.name === 'add') {
        this.editDialogTitle = this.titles.add;
        this.editingRowURL = this.detail_url.replace('--record_id--', 'new').replace('.json', '.componentdef');
        DynamicForms.dialog.fromURL(this.editingRowURL, null, this.uuid);
      } else {
        this.editDialogTitle = `unknown action ${action.name}... so, a stupid title`;
        this.editingRowURL = '';
      }
    },
    setTableFilter(filter) {
      // console.log(filter);
      this.filterQueryString = $.param(_.pickBy(
        _.clone(filter.filter), (v) => (_.isString(v) ? _.size(v) : v !== null && v !== undefined),
      ));
      if (filter.doFilter) {
        this.loadData();
      }
    },
    tableAction(payload) {
      if (['add', 'edit', 'delete', 'filter', 'submit', 'cancel'].includes(payload.action.name)) {
        this.executeTableAction(payload.action, payload.data, payload.modal, {});
      } else {
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
    },
  },
};
</script>

<style scoped>

</style>
