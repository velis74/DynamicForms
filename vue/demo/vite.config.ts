/// <reference types="vitest" />
import { resolve } from 'path';

import vue from '@vitejs/plugin-vue';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { ConfigEnv, defineConfig, loadEnv } from 'vite';
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
        target: process.env.VITE_AXIOS_TARGET,
        changeOrigin: false,
        pathRewrite: (path) => (path),
      }),
    );
  },
});

export default ({ mode }: ConfigEnv) => {
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };
  return defineConfig({
    plugins: [
      vue(),
      {
        ...eslint({
          failOnWarning: false,
          failOnError: false,
          overrideConfig: { parserOptions: { project: '../../tsconfig.eslint.json' } },
        }),
        apply: 'serve',
        enforce: 'post',
      },
      vuetify({ autoImport: true }),
      axiosRedirectConfig(),
    ],
    resolve: {
      alias: {
        dynamicforms: resolve(__dirname, '../dynamicforms/src/index'),
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
};
