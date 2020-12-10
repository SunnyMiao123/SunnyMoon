import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import router from './router'
import elementui from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import elTableInfiniteScroll from 'el-table-infinite-scroll';
import store from './store'

Vue.config.productionTip = false
axios.defaults.baseURL="http://127.0.0.1:8101/"
Vue.prototype.$axios=axios
Vue.use(VueRouter)
Vue.use(elementui)
Vue.use(elTableInfiniteScroll)
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
