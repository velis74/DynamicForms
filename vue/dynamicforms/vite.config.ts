/// <reference types="vitest" />
import { resolve } from 'path';

import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';
import eslint from 'vite-plugin-eslint';
import vuetify  from 'vite-plugin-vuetify';

/** @type {import('vite').UserConfig} */
export default defineConfig({
  plugins: [
    vue(),
    {
      ...eslint({
        failOnWarning: false,
        failOnError: false,
      }),
      apply: 'serve',
      enforce: 'post',
    },
    vuetify({ autoImport: true }),
  ],
  resolve: {
    // alias: {
    //   '@': fileURLToPath(new URL_('./src', import.meta.url)),
    //   '~': fileURLToPath(new URL_('./node_modules', import.meta.url)),
    // },
    extensions: [
      '.js',
      '.ts',
      '.vue',
      '.json',
      '.css',
    ],
  },
  build: {
    target: 'es2022',
    lib: {
      entry: resolve(__dirname, './src/dynamicforms.ts'),
      formats: ['umd'],
      fileName: 'dynamicforms',
      name: 'dynamicforms.[name]',
    },
    rollupOptions: {
      external: ['axios', 'bootstrap', 'bootstrap-vue', 'lodash', 'vue', 'vue-ionicon', 'vue-router', 'vuetify'],
      output: {
        sourcemap: true,
        globals: (id: string) => id, // all external modules are currently not aliased to anything but their own names
      }
    }
  },
  test: {
    deps: {
      inline: ['vuetify']
    },
    globals: true,
    environment: 'jsdom',
    useAtomics: true, // eliminate tests hang at the end (https://github.com/vitest-dev/vitest/issues/2008)
  },
});
