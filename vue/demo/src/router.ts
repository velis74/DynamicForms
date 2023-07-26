import { createRouter, createWebHashHistory, RouteLocationNormalized } from 'vue-router';

import routes from './routes';

const router = createRouter({
  // @ts-ignore
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

router.afterEach((to: RouteLocationNormalized) => {
  document.title = String(to.meta.title || 'Vite App');
});

export default router;
