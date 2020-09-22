import Vue from 'vue'
import ElementUi from 'element-ui'
import locale from 'element-ui/lib/locale/lang/ja'
import 'element-ui/lib/theme-chalk/index.css'
import 'element-ui/lib/theme-chalk/display.css'

import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.devtools = true;
Vue.config.productionTip = process.env.NODE_ENV === 'production';

Vue.use(ElementUi, { locale });


new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
