import Vue from 'vue'
import Router from 'vue-router'
import Entry from '../components/Entry.vue'
import Dashboard from '../components/Dashboard.vue'
import { authRequired, User } from '../service'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Entry',
      component: Entry,
      beforeEnter (to, from, next) {
        if (User.isAuthenticated()) {
          next({
            path: '/dashboard'
          })
        } else {
          next()
        }
      }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      beforeEnter: authRequired
    }
  ]
})
