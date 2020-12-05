import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import HelloWorld from '../components/HelloWorld.vue'
import task from '../components/taskdisplay.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path:'/HelloWorld',
    name:'HelloWorld',
    component:HelloWorld
  },
  {
    path:'/task',
    name:'task',
    component:task
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode:'history',
  routes
})

export default router
