import VueRouter from 'vue-router'

import NotFound from '@/components/NotFound.vue'
import Signup from '@/views/authentication/Signup.vue'
import Login from '@/views/authentication/Login.vue'
import BreakBreadSurveyList from '@/views/breakbread-list/BreakBreadSurveyList.vue'
import SurveyForm from '@/views/potluck-survey/SurveyForm.vue'
import auth from '@/services/auth'
import Groups from '@/views/potluck-group/Groups'
import Potlucks from '@/views/potluck-group/Potlucks'
import FoodList from '@/views/potluck-food/FoodList.vue'
import SelectFood from '@/views/select-food/SelectFood.vue'
const routes = [
  {
    path: '/',
    component: BreakBreadSurveyList
  },
  {
    path: '/signup',
    component: Signup,
    meta: { layout: 'no-sidebar' }
  },
  {
    path: '/login',
    component: Login,
    meta: { layout: 'no-sidebar', isPublic: true }
  },
  {
    path: '/survey-list',
    component: BreakBreadSurveyList
  },
  {
    path: '/survey-form',
    component: SurveyForm,
    meta: { layout: 'no-sidebar', isPublic: true }
  },
  {
    path: '/select-food/group/:group_id/user/:user_id',
    component: SelectFood,
    meta: { layout: 'no-sidebar', isPublic: true }
  },
  {
    path: '/groups',
    component: Groups
  },
  {
    path: '/potlucks',
    component: Potlucks
  },
  {
    path: '/food-list',
    component: FoodList
  },
  {
    path: '*',
    component: NotFound,
    meta: { layout: 'no-sidebar', isPublic: true }
  }
]
const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const authRequired = !to.meta.isPublic
  auth.checkAuth()
  const loggedIn = auth.user.authenticated
  if (authRequired && !loggedIn) {
    return next('/login')
  } else if (loggedIn && to.path === '/login') {
    return next('/')
  }
  return next()
})

export { router, VueRouter }
