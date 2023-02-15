import APIConsumerLoader from './components/api_consumer/api-consumer-loader.vue';
import ModalDemo from './demo-app/modal-demo.vue';
import NamedComponentLoader from './demo-app/named-component-loader.vue';

const EmptyComponent = { render() { return null; } };

export default [
  { name: 'home', path: '/', component: EmptyComponent, meta: { title: 'Home' } },
  { name: 'CL Validated', path: '/validated', component: APIConsumerLoader, meta: { title: 'Validated' } },
  { name: 'CL Hidden fields', path: '/hidden-fields', component: APIConsumerLoader, meta: { title: 'Hidden fields' } },
  { name: 'CL Basic fields', path: '/basic-fields', component: APIConsumerLoader, meta: { title: 'Basic fields' } },
  {
    name: 'CL Advanced fields',
    path: '/advanced-fields',
    component: APIConsumerLoader,
    meta: { title: 'Advanced fields' },
  },
  { name: 'CL Page loading', path: '/page-load', component: APIConsumerLoader, meta: { title: 'Page loading' } },
  { name: 'CL Filtering', path: '/filter', component: APIConsumerLoader, meta: { title: 'Filtering' } },
  {
    name: 'Actions overview',
    path: '/actions-overview',
    component: APIConsumerLoader,
    meta: { title: 'Actions overview' },
  },
  {
    name: 'CL Custom CSS per row',
    path: '/calculated-css-class-for-table-row',
    component: APIConsumerLoader,
    meta: { title: 'Custom CSS per row' },
  },
  // { path: '/single-dialog/:id', component: PageLoader, meta: { component: 'dialog', uuid: singleDlgFakeUUID } },
  // { path: '/choice-allow-tags-fields', component: PageLoader },
  // { path: '/calendar', component: Calendar },
  // { path: '/documents', component: PageLoader },
  { name: 'Modal dialogs', path: '/modal', component: ModalDemo, meta: { title: 'Modal dialogs' } },
  {
    name: 'The three view-modes',
    path: '/view-mode',
    component: NamedComponentLoader,
    props: { componentName: 'DfViewMode', componentProps: {} },
    meta: { title: 'The three view-modes' },
  },
];
