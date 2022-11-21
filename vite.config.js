import { resolve } from 'path';
import { defineConfig } from 'vite';
import { createVuePlugin as vue2 } from 'vite-plugin-vue2';
import Components from 'unplugin-vue-components/vite';
import { VuetifyResolver } from 'unplugin-vue-components/resolvers';
import eslint from 'vite-plugin-eslint';

const { createProxyMiddleware } = require('http-proxy-middleware');
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
    vue2({
      jsx: true,
    }),
    {
      ...eslint({
        failOnWarning: false,
        failOnError: false
      }),
      apply: 'serve',
      enforce: 'post'
    },
    Components({
      resolvers: [VuetifyResolver()]
    }),
    axiosRedirectConfig()
  ],
  resolve: {
    alias: [
      {
        find: /^~(.*)$/,
        replacement: 'node_modules/$1',
      },
    ],
    extensions: [
      ".js",
      ".vue",
      ".json"
    ],
  },
  server: {
    port: 8080,
  //   proxy: {
  //     "^.*\.(json|componentdef)": {
  //       "target": "http://localhost:8000",
  //       changeOrigin: true,
  //       "secure": false,
  //       rewrite: path => {
  //         console.log(path);
  //         return path;
  //       }
  //     }
  //   }
  },
  build: {
    lib: {
      entry: resolve(__dirname, "./vue/main.js"),
      fileName: 'js/dynamicforms.[hash:8].js',
      name: 'dynamicforms.[name]'
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        globals: {
          vue: "Vue"
        }
      }
    },
  },
  test: {
    globals: true,
    environment: 'jsdom',
  }
});
