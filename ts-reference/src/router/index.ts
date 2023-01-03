import { createRouter, createWebHashHistory } from 'vue-router'
import routes from '@/routes'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: routes,
});

router.afterEach((to) => {
  document.title = String(to.meta.title || "Vite App");
});

export default router;
