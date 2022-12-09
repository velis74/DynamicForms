import { fileURLToPath, URL } from 'node:url'

import { createProxyMiddleware } from 'http-proxy-middleware';
import { resolve } from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify';
import eslint from 'vite-plugin-eslint';

const axiosRedirectConfig = () => ({
  name: 'serverProxy',
  configureServer(server) {
    const filter = function (pathname, req) {
      return typeof req.headers['x-csrftoken'] != 'undefined'
    }
    server.middlewares.use(
      '/',
      createProxyMiddleware(filter, {
        target: 'http://localhost:8000',
        changeOrigin: false,
        pathRewrite: path => {
          console.log('path', path);
          return path;
        }
      })
    )
  }
});

/** @type {import('vite').UserConfig} */
export default defineConfig({
  plugins: [
    vue({ template: transformAssetUrls }),
    {
      ...eslint({
        failOnWarning: false,
        failOnError: false
      }),
      apply: 'serve',
      enforce: 'post'
    },
    vuetify({ autoImport: true }),
    axiosRedirectConfig()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~': fileURLToPath(new URL('./node_modules', import.meta.url)),
    },
    extensions: [
      '.js',
      '.vue',
      '.json',
      '.css'
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
    lib: {
      entry: resolve(__dirname, "./vue/main.js"),
      fileName: 'js/dynamicforms.[hash:8].js',
      name: 'dynamicforms.[name]'
    },
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router'],
          vuetify: [
            'vuetify',
            'vuetify/components',
            'vuetify/directives',
          ],
        }
      }
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
  }
});
