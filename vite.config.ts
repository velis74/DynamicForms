/// <reference types="vitest" />
import { fileURLToPath, URL as URL_ } from 'node:url';
import { resolve } from 'path';

import vue from '@vitejs/plugin-vue';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { defineConfig } from 'vite';
import eslint from 'vite-plugin-eslint';
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify';

const axiosRedirectConfig = () => ({
  name: 'serverProxy',
  configureServer(server: any) {
    const filter = function filter(pathname: any, req: any) {
      return typeof req.headers['x-df-axios'] !== 'undefined' || pathname.startsWith("/calendar-event");
    };
    server.middlewares.use(
      '/',
      createProxyMiddleware(filter, {
        target: 'http://localhost:8000',
        changeOrigin: false,
        pathRewrite: (path) => {
          // console.log('path', path);
          return path;
        },
      }),
    );
  },
});

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
    axiosRedirectConfig(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL_('./src', import.meta.url)),
      '~': fileURLToPath(new URL_('./node_modules', import.meta.url)),
    },
    extensions: [
      '.js',
      '.ts',
      '.vue',
      '.json',
      '.css',
    ],
  },
  server: {
    port: 8080,
    fs: {
      // Allow serving files from one level up to the project root
      allow: ['..'],
    },
  },
  build: {
    target: 'es2022',
    lib: {
      entry: resolve(__dirname, './vue/dynamicforms.ts'),
      formats: ['umd'],
      fileName: 'dynamicforms',
      name: 'dynamicforms.[name]',
    },
    rollupOptions: {
      external: ['vue', 'vue-router', 'vuetify'],
      output: {
        sourcemap: true,
        globals: {
          vue: 'vue',
          'vue-router': 'vue-router',
          vuetify: 'vuetify'
        }
      }
    }
  },
  test: {
    deps: {
      inline: ['vuetify']
    },
    globals: true,
    environment: 'jsdom',
    useAtomics: true, // eliminates tests hang at the end (https://github.com/vitest-dev/vitest/issues/2008)
  },
});
