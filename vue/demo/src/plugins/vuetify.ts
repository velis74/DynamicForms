import { createVuetify } from 'vuetify';
import { ThemeDefinition } from 'vuetify/dist/vuetify';

const defaultTheme: ThemeDefinition = {
  dark: false,
  colors: {
    background: '#f8f8f8',
    surface: '#ffffff',
    // 'primary-darken-1': '#3700B3',
    // 'secondary-darken-1': '#018786',
    primary: '#3f51b5',
    secondary: '#2196f3',
    accent: '#ffc107',
    error: '#f44336',
    warning: '#ff9800',
    info: '#8bc34a',
    success: '#00bcd4',
  },
};

const vuetify = createVuetify({
  defaults: { global: {} },
  theme: { defaultTheme: 'defaultTheme', themes: { defaultTheme } },
});

export default vuetify;
