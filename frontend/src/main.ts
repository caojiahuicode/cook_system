import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import './index.css';

// Views
import Dashboard from './views/Dashboard.vue';
import Library from './views/Library.vue';
import RecipeDetail from './views/RecipeDetail.vue';
import Login from './views/Login.vue';
import Settings from './views/Settings.vue';

const routes = [
  { path: '/', component: Dashboard },
  { path: '/library', component: Library },
  { path: '/recipe/:id', component: RecipeDetail },
  { path: '/login', component: Login },
  { path: '/settings', component: Settings },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const app = createApp(App);
app.use(router);
app.mount('#root');
