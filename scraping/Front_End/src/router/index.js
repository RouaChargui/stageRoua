import { createRouter, createWebHistory } from 'vue-router';
import LoginAuth from '@/components/LoginAuth.vue';
import YouRegister from '@/components/YouRegister.vue';  // Assurez-vous que le chemin est correct
import MyHome from '@/components/MyHome.vue';
import PageAcc from '@/components/PageAcc.vue';

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginAuth,
  },
  {
    path: '/home',
    name: 'home',
    component: MyHome,
    beforeEnter: (to, from, next) => {
      // Vérifie si un token est présent
      if (!localStorage.getItem('authToken')) {
        next({ name: 'login' });  // Redirige vers login si aucun token
      } else {
        next();  // Permet l'accès à /home si le token existe
      }
    }
  },
  {
    path: '/register',
    name: 'register',
    component: YouRegister,
  },
  {
    path: '/pageAcc',
    name: 'pageacc',
    component: PageAcc,
    beforeEnter: (to, from, next) => {
      // Vérifie si un token est présent
      if (!localStorage.getItem('authToken')) {
        next({ name: 'login' });  // Redirige vers login si aucun token
      } else {
        next();  // Permet l'accès à /pageAcc si le token existe
      }
    }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
