/// <reference types="vitest" />
import { resolve } from 'path';

import vue from '@vitejs/plugin-vue';
import dts from 'vite-plugin-dts';
import { defineConfig } from 'vite';
import eslint from 'vite-plugin-eslint';
import vuetify  from 'vite-plugin-vuetify';

/** @type {import('vite').UserConfig} */
export default defineConfig({
  plugins: [
    vue(),
    // dts(),  // enable when TS errors are no longer present
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
    alias: {
      '@': resolve(__dirname, './src'),
      '~': resolve(__dirname, '../../node_modules'),
    },
    extensions: [
      '.js',
      '.ts',
      '.vue',
      '.json',
      '.css',
    ],
  },
  build: {
    target: 'es2015',
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      formats: ['umd', 'es'],
      fileName: 'dynamicforms',
      name: 'dynamicforms.[name]',
    },
    rollupOptions: {
      external: [
        'axios',
        'bootstrap',
        'bootstrap-vue',
        '@ckeditor/ckeditor5-autoformat',
        '@ckeditor/ckeditor5-basic-styles',
        '@ckeditor/ckeditor5-block-quote',
        '@ckeditor/ckeditor5-editor-classic',
        '@ckeditor/ckeditor5-essentials',
        '@ckeditor/ckeditor5-heading',
        '@ckeditor/ckeditor5-image',
        '@ckeditor/ckeditor5-indent',
        '@ckeditor/ckeditor5-link',
        '@ckeditor/ckeditor5-list',
        '@ckeditor/ckeditor5-paragraph',
        '@ckeditor/ckeditor5-table',
        '@ckeditor/ckeditor5-theme-lark',
        '@ckeditor/ckeditor5-typing',
        '@ckeditor/ckeditor5-upload',
        '@ckeditor/ckeditor5-vue',
        'lodash',
        'vue',
        'vue-ionicon',
        'vue-router',
        'vuetify'
      ],
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
