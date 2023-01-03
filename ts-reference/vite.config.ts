import { fileURLToPath, URL } from 'node:url'

import { createProxyMiddleware } from 'http-proxy-middleware';
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify';
import checker from "vite-plugin-checker";

const axiosRedirectConfig = () => ({
  name: 'serverProxy',
  configureServer(server: any) {
    const filter = function (pathname: any, req: any) {
      return typeof req.headers['x-csrftoken'] != 'undefined'
    }
    server.middlewares.use(
      '/',
      createProxyMiddleware(filter, {
        target: 'http://localhost:8000',
        changeOrigin: false,
      })
    )
  }
});

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({template: transformAssetUrls,}),
    vuetify({autoImport: true,}),
    checker({
      typescript: true,
      vueTsc: true,
      eslint: {lintCommand: 'eslint "./src/*.{ts,tsx,js,jsx,vue}'}
    }),
    axiosRedirectConfig()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~': fileURLToPath(new URL('./node_modules', import.meta.url)),
    }
  },
  server: {
    fs: {
      // Allow serving files from one level up to the project root
      allow: ['..'],
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vue: ['vue', 'vue-router'],
          vuetify: [
            'vuetify',
            'vuetify/components',
            'vuetify/directives',
          ],
          materialdesignicons: ['@mdi/font/css/materialdesignicons.css'],
        }
      }
    }
  },
})
