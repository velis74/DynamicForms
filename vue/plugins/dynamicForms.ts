import { createDynamicForms } from '../dynamicforms/src/dynamicforms';
import type { DynamicFormsOptions } from '../dynamicforms/src/dynamicforms';

const options: DynamicFormsOptions = { ui: 'vuetify' };

export default createDynamicForms(options);
