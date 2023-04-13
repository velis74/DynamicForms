import { inject } from 'vue';

// eslint-disable-next-line import/no-named-default
import { default as bootstrapBP } from './breakpoints-bootstrap';
import BreakpointsInterface from './breakpoints-interface';
// eslint-disable-next-line import/no-named-default
import { default as vuetifyBP } from './breakpoints-vuetify';

// eslint-disable-next-line import/prefer-default-export
export function useDisplay(): BreakpointsInterface {
  const theme = inject('$df$ApplicationTheme') as string;
  switch (theme) {
  case 'vuetify':
    return vuetifyBP();
  case 'bootstrap':
    return bootstrapBP();
  default:
    return vuetifyBP();
  }
}
