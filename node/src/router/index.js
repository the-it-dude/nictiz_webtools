import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/epd',
    name: 'EPD',
    component: () => import('../views/Epd/index.vue')
  },
  {
    path: '/terminologie/searchComments',
    name: 'Zoek commentaar in Termspace',
    component: () => import('../views/Terminologie/TermspaceComments.vue')
  },
  {
    path: '/terminologie/mappingComments',
    name: 'Zoek commentaar in mappingtool',
    component: () => import('../views/Terminologie/MappingComments.vue')
  },
  {
    path: '/mapping/RcAudit',
    name: 'Mapping release candidate audit',
    component: () => import('../views/Mapping/RcAudit.vue')
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue')
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
})

export default router
