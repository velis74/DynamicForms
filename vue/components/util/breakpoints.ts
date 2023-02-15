import { inject } from 'vue';

// eslint-disable-next-line import/no-named-default
import { default as bootstrapBP } from './breakpoints-bootstrap';
// eslint-disable-next-line import/no-named-default
import { default as vuetifyBP } from './breakpoints-vuetify';

export default function useDisplay() {
  const theme = inject('$df$ApplicationTheme') as string;
  switch (theme) {
  case 'vuetify':
    return vuetifyBP;
  case 'bootstrap':
    return bootstrapBP;
  default:
    return vuetifyBP;
  }
}
