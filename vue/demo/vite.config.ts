/// <reference types="vitest" />
import { resolve } from 'path';

import vue from '@vitejs/plugin-vue';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { defineConfig } from 'vite';
import eslint from 'vite-plugin-eslint';
import vuetify from 'vite-plugin-vuetify';

const axiosRedirectConfig = () => ({
  name: 'serverProxy',
  configureServer(server: any) {
    const filter = function filter(pathname: any, req: any) {
      return typeof req.headers['x-df-axios'] !== 'undefined' || pathname.startsWith('/calendar-event');
    };
    server.middlewares.use(
      '/',
      createProxyMiddleware(filter, {
        target: 'http://localhost:8000',
        changeOrigin: false,
        pathRewrite: (path) => (path),
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
    alias: { dynamicforms: resolve(__dirname, '../dynamicforms/src/dynamicforms') },
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
  test: {
    deps: { inline: ['vuetify'] },
    globals: true,
    environment: 'jsdom',
    useAtomics: true, // eliminates tests hang at the end (https://github.com/vitest-dev/vitest/issues/2008)
  },
});
