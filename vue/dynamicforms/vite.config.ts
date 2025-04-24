/// <reference types="vitest" />
import vue from '@vitejs/plugin-vue';
import * as path from 'node:path';
import { resolve } from 'path';
import { defineConfig, searchForWorkspaceRoot } from 'vite';
import eslint from 'vite-plugin-eslint';
import vuetify from 'vite-plugin-vuetify';
import { visualizer } from 'rollup-plugin-visualizer';

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
    visualizer({
      open: false,
      filename: 'coverage/stats.html',
      gzipSize: true,
      brotliSize: true,
    }),
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src/components'),
      '~': resolve(__dirname, '../../node_modules'),
    },
    extensions: [
      '.js',
      '.mjs',
      '.ts',
      '.vue',
      '.json',
      '.css',
    ],
  },
  build: {
    target: 'es2015',
    sourcemap: true,
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      formats: ['umd', 'es'],
      fileName: 'dynamicforms',
      name: 'dynamicforms.[name]',
    },
    rollupOptions: {
      external: [
        '@dynamicforms/vue-forms',
        '@dynamicforms/vuetify-inputs',
        '@ckeditor/ckeditor5-vue',
        '@kyvg/vue3-notification',
        'ckeditor5',
        'axios',
        'bootstrap',
        'bootstrap-vue',
        'date-fns',
        'lodash-es',
        'resize-observer-polyfill',
        'vue',
        'vue-ionicon',
        'vue-markdown-render',
        'vue-router',
        /^vuetify\/.*/,
      ],
      output: {
        globals: (id: string) => id, // all external modules are currently not aliased to anything but their own names
      }
    }
  },
  test: {
    server: {
      deps: {
        inline: [/vuetify/]
      },
    },
    globals: true,
    environment: 'jsdom',
    exclude: ['**/*.css'],
  },
});
