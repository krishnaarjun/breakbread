import Vue from 'vue'
import iView from 'iview'
import moment from 'moment'
import 'iview/dist/styles/iview.css'
import locale from 'iview/dist/locale/en-US'
import App from '@/App.vue'
import { router, VueRouter } from '@/routes'
import Default from '@/layouts/Default'
import NoSidebar from '@/layouts/NoSidebar'

Vue.use(VueRouter)

Vue.use(iView, {
  locale: locale
})

Vue.component('default-layout', Default)
Vue.component('no-sidebar-layout', NoSidebar)
Vue.filter('formatDate', value => {
  if (value) {
    return moment(String(value)).format('MM-DD-YYYY')
  }
})
new Vue({ el: '#app', router, render: h => h(App) }) // eslint-disable-line no-new

export default router
