/// <reference types="vitest" />
import { fileURLToPath, URL as URL_ } from 'node:url';
import { resolve } from 'path';

import vue from '@vitejs/plugin-vue';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { ConfigEnv, defineConfig, loadEnv } from 'vite';
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
        target: process.env.VITE_AXIOS_TARGET,
        changeOrigin: false,
        pathRewrite: (path) => {
          // console.log('path', path);
          return path;
        },
      }),
    );
  },
});

export default ({mode}: ConfigEnv) => {
  process.env = {...process.env, ...loadEnv(mode, process.cwd())};
  return defineConfig({
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
      vuetify({autoImport: true}),
      axiosRedirectConfig(),
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
      useAtomics: true, // eliminates tests hang at the end (https://github.com/vitest-dev/vitest/issues/2008)
    },
  });
};
