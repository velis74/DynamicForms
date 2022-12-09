import APIConsumerLoader from './components/api_consumer/api-consumer-loader';
import ModalDemo from './demo-app/modal-demo';
import NamedComponentLoader from './demo-app/named-component-loader';

export default [
  { name: 'Validated', path: '/validated', component: APIConsumerLoader, meta: { title: 'Validated' } },
  { name: 'Hidden fields', path: '/hidden-fields', component: APIConsumerLoader, meta: { title: 'Hidden fields' } },
  { name: 'Basic fields', path: '/basic-fields', component: APIConsumerLoader, meta: { title: 'Basic fields' } },
  {
    name: 'Advanced fields',
    path: '/advanced-fields',
    component: APIConsumerLoader,
    meta: { title: 'Advanced fields' },
  },
  { name: 'Page loading', path: '/page-load', component: APIConsumerLoader, meta: { title: 'Page loading' } },
  { name: 'Filtering', path: '/filter', component: APIConsumerLoader, meta: { title: 'Filtering' } },
  {
    name: 'Actions overview',
    path: '/actions-overview',
    component: APIConsumerLoader,
    meta: { title: 'Actions overview' },
  },
  {
    name: 'Custom CSS per row',
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
    props: { componentName: 'ViewMode', componentNameAddTemplateName: true, componentProps: {} },
    meta: { title: 'The three view-modes' },
  },
];
