import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import router from './router'
import elementui from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'

Vue.config.productionTip = false
Vue.prototype.$axios=axios
Vue.use(VueRouter)
Vue.use(elementui)
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
