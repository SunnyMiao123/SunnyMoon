import Vue from 'vue'
import VueRouter from 'vue-router'
import task from '../components/taskdisplay.vue'
import home from '../components/home.vue'
import projects from '../components/projects.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: home
  },

  {
    path:'/task',
    name:'task',
    component:task
  },
  {
    path:'/projects',
    name:'projects',
    component:projects
  }
]

const router = new VueRouter({
  mode:'history',
  routes
})

export default router
