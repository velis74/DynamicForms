import { defineComponent } from 'vue';

import FilteredActions from '../actions/filtered-actions';

import FormPayload from './definitions/form-payload';
import FormLayoutClass from './definitions/layout';

export default /* #__PURE__ */ defineComponent({
  name: 'FormMixin',
  props: {
    title: { type: String, required: true }, // form title to be displayed (e.g. in the header)
    pkName: { type: String, required: true }, // field name that contains the primary key value
    pkValue: { type: null, required: true }, // value of primary key (used to assemble GET/PUT URLs)
    layout: { type: FormLayoutClass, required: true }, // layout definition
    payload: { type: FormPayload, required: true }, // form data
    actions: { type: FilteredActions, default: null }, // form actions
    errors: { type: Object, default: () => {} }, // form errors (usually after a 400 response)
  },
});
