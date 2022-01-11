<template>
  <div>
    <div id="titlebar">
      <div id="hamburger" @click.stop="menuShown = !menuShown">
        &#9776; <span id="page-title">{{ title }}</span>
      </div>
    </div>
    <transition name="fade">
      <div v-if="menuShown" class="sidenav-group">
        <div id="sidenav-overlay" @click.stop="menuShown = !menuShown"/>
        <div id="side-nav" class="sidenav">
          <router-link to="/validated">Validated</router-link>
          <router-link to="/hidden-fields">Hidden fields</router-link>
          <router-link to="/basic-fields">Basic fields</router-link>
          <router-link to="/advanced-fields">Advanced fields</router-link>
          <router-link to="/page-load">Page loading</router-link>
          <router-link to="/filter">Filter</router-link>
          <a href="#" @click.stop="showSingleDialog">Pop-up dialog</a>
          <a href="#" onclick="singleDialog()">Choice allow tags dialog</a>
          <router-link to="/refresh-types">Refresh types</router-link>
          <router-link to="/calculated-css-class-for-table-row">Row css style</router-link>
          <router-link to="/choice-allow-tags-fields">Tag select fields</router-link>
          <router-link to="/calendar">Calendar example</router-link>
          <router-link to="/documents">Documents</router-link>
          <router-link to="/view-mode">The three view modes</router-link>
        </div>
      </div>
    </transition>
    <div id="main">
      <router-view @title-change="(val) => { title = val; }" @load-route="loadRoute"/>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import VueRouter from 'vue-router';

import apiClient from '../apiClient';
import DynamicForms from '../dynamicforms';
import eventBus from '../logic/eventBus';

import Calendar from './calendar.vue';
import ExampleHiddenLayout from './example_hidden_layout.vue';
import PageLoader from './pageloader.vue';
import SingleDialog from './single_dialog.vue';
import ViewMode from './viewmode.vue';

Vue.use(VueRouter);
// we must register custom components or they won't show
Vue.component(SingleDialog.name, SingleDialog);
Vue.component(ExampleHiddenLayout.name, ExampleHiddenLayout);
Vue.component(Calendar.name, Calendar);

const singleDlgFakeUUID = 'fake-uuid-654654-634565';
const routes = [
  { path: '/validated', component: PageLoader },
  { path: '/hidden-fields', component: PageLoader },
  { path: '/basic-fields', component: PageLoader },
  { path: '/advanced-fields', component: PageLoader },
  { path: '/page-load', component: PageLoader },
  { path: '/filter', component: PageLoader },
  { path: '/refresh-types', component: PageLoader },
  { path: '/calculated-css-class-for-table-row', component: PageLoader },
  { path: '/single-dialog/:id', component: PageLoader, meta: { component: 'dialog', uuid: singleDlgFakeUUID } },
  { path: '/choice-allow-tags-fields', component: PageLoader },
  { path: '/calendar', component: Calendar },
  { path: '/documents', component: PageLoader },
  { path: '/view-mode', component: ViewMode },
];
const router = new VueRouter({ routes });

export default {
  name: 'Example',
  components: {},
  router,
  data() {
    return {
      menuShown: false,
      title: '',
      currentFormUUID: null,
    };
  },
  watch: {
    $route() {
      this.menuShown = false;
    },
  },
  mounted() {
    if (router.history.current.path === '/') {
      router.push('/validated');
    }
    eventBus.$on(`tableActionExecuted_${singleDlgFakeUUID}`, this.singleDialogBtnClick);
    eventBus.$on('showingRESTForm', this.showingRESTForm);
  },
  beforeDestroy() {
    eventBus.$off('showingRESTForm');
    eventBus.$off(`tableActionExecuted_${singleDlgFakeUUID}`);
  },
  methods: {
    showSingleDialog() {
      this.menuShown = !this.menuShown;
      DynamicForms.dialog.fromURL('/single-dialog/new.component', 'new', singleDlgFakeUUID);
    },
    loadRoute(path, uuid) {
      eventBus.$off(`fieldValueChanged${this.currentFormUUID}`);
      this.currentFormUUID = uuid;
      eventBus.$on(`fieldValueChanged${this.currentFormUUID}`, this.fieldValueChanged);
    },
    singleDialogBtnClick(payload) {
      if (payload.action.name === 'say_it') {
        apiClient
          .post('/single-dialog.json', payload.data)
          .then((res) => {
            alert(res.data.test); // eslint-disable-line no-alert
            payload.modal.hide();
          });
      } else if (payload.action.name === 'download') {
        payload.data.download = '1';
        apiClient
          .post('/single-dialog.json', payload.data)
          .then((res) => {
            // get the filename from content-disposition
            let filename = '';
            const disposition = res.headers['Content-Disposition'];
            if (disposition && disposition.indexOf('attachment') !== -1) {
              const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
              const matches = filenameRegex.exec(disposition);
              if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
              }
            }

            // create a local download link
            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename); // or any other extension
            link.innerHTML = filename;
            document.body.appendChild(link);
            link.click();

            // close the dialog
            payload.modal.hide();
          });
      } else if (payload.action.name === 'cancel') {
        payload.modal.hide();
      }
    },
    fieldValueChanged(payload) {
      console.log('FieldValueChanged', payload);
    },
    showingRESTForm(payload) {
      if (payload.tableUUID === this.currentFormUUID) {
        eventBus.$on(`fieldValueChanged${payload.formUUID}`, this.fieldValueChanged);
      }
    },
  },
};

</script>

<style scoped>
.sidenav-group {
  position: relative;
  z-index:  100;
}

.sidenav {
  width:            20rem;
  position:         fixed;
  z-index:          2;
  top:              3.5em;
  left:             0;
  bottom:           0;
  background-color: #111;
  overflow-x:       hidden;
}

.sidenav a {
  padding:         .5rem;
  text-decoration: none;
  font-size:       1.75rem;
  white-space:     nowrap;
  color:           #818181;
  display:         block;
}

#sidenav-overlay {
  z-index:    1;
  background: black;
  position:   fixed;
  left:       0;
  top:        3.5em;
  width:      100%;
  height:     100%;
  opacity:    0.2;
}

.sidenav a:hover {
  color: #f1f1f1;
}

#main {
  transition: margin-left .5s;
  padding:    1rem;
  margin-top: 3.5rem;
}

#hamburger {
  font-size: 200%;
  cursor:    pointer;
}

#titlebar {
  position:     absolute;
  z-index:      3;
  top:          0;
  left:         0;
  right:        0;
  background:   darkslategrey;
  height:       3.5em;
  padding-left: 1em;
  color:        white;
}

/* these selectors are used in the transition */
/*noinspection CssUnusedSymbol*/
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}

/*noinspection CssUnusedSymbol*/
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
