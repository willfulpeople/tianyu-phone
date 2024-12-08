import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/info-square',
    name: 'InfoSquare',
    component: () => import('../views/InfoSquare.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/recycle',
    name: 'Recycle',
    component: () => import('../views/Recycle.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/phone-share',
    name: 'PhoneShare',
    component: () => import('../views/PhoneShare.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path)
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    console.log('Auth required, redirecting to login')
    next('/login')
  } else if (to.path === '/login' && token) {
    console.log('Already logged in, redirecting to home')
    next('/')
  } else {
    console.log('Navigation allowed')
    next()
  }
})

export default router