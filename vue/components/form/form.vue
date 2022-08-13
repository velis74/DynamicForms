<script>
import FilteredActions from '../actions/filtered-actions';

import FormPayload from './definitions/form_payload';
import FormLayoutClass from './definitions/layout';

export default {
  name: 'FormMixin',
  props: {
    pkName: { type: String, required: true },
    title: { type: String, required: true },
    pkValue: { type: null, required: true },
    layout: { type: FormLayoutClass, required: true },
    payload: { type: FormPayload, required: true },
    actions: { type: FilteredActions, default: null },
  },
};
</script>
