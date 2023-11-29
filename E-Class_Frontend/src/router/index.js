import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

import HomePage from '@/views/HomePage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: { path: '/realhome' }
    },
    {
      path: '/home',
      name: 'Home',
      component: HomePage,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginPage.vue')
    },
    {
      path: '/forgot-password',
      name: 'ForgotPassword',
      component: () => import('@/views/ForgotPasswordPage.vue')
    },
    {
      // add "/" to the end of the path to prevent 404 error due to the dot in the token
      path: '/reset-password/:reset_password_token/',
      name: 'ResetPassword',
      component: () => import('@/views/ResetPasswordPage.vue')
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: () => import('@/views/SignUpPage.vue')
    },
    {
      //added as one of the main routes, but should be a children of the viewCourse route.
      path: '/apply-course',
      name: 'ApplyCourse',
      component: () => import('@/views/ApplyCoursePage.vue')
    },
    {
      path: '/search-course',
      redirect: '/search-course/wow_nothing_here'
    },
    {
      //added as one of the main routes, but should be a children of the viewCourse route.
      path: '/search-course/:search_content',
      name: 'Search-course',
      component: () => import('@/views/SearchCoursePage.vue')
    },
    {
      path: '/main',
      component: () => import('@/views/MainPage.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'Main',
          redirect: { path: '/main/dashboard' }
        },
        {
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/main/DashboardSection.vue')
        },
        {
          path: 'courses/',
          name: 'Courses',
          component: () => import('@/views/main/CoursesSection.vue'),
          children: [
            {
              path: ':course_id/',
              component: () => import('@/views/main/CourseDetail.vue')
            }
          ]
        },
        {
          path: 'messages',
          name: 'Messages',
          component: () => import('@/views/main/MessagesSection.vue')
        },
        {
          path: 'account',
          component: () => import('@/views/main/AccountSection.vue'),
          children: [
            {
              path: '',
              name: 'Account',
              redirect: { path: '/main/account/profile' }
            },
            {
              path: 'profile',
              name: 'Profile',
              component: () => import('@/views/main/account/ProfilePage.vue')
            },
            {
              path: 'payments',
              name: 'Payments',
              component: () => import('@/views/main/account/PaymentsPage.vue')
            },
            {
              path: 'invoices',
              name: 'Invoices',
              component: () => import('@/views/main/account/InvoicesPage.vue')
            }
          ]
        }
        // Add more sections as needed
      ]
    },
    {
      path: '/viewcoursepage/',
      redirect: '/'
    },
    {
      path: '/viewcoursepage/:course_id',
      name: 'Viewcourse',
      component: () => import('@/views/ViewCoursePage.vue')
    },
    {
      path: '/reviewcoursepage',
      name: 'reviewcourse',
      component: () => import('@/views/ReviewCoursePage.vue')
    },
    {
      path: '/realhome',
      name: 'RealHome',
      component: () => import('@/views/RealHomePage.vue')
    },
    {
      path: '/fqa',
      name: 'Fqa',
      component: () => import('@/views/FaqPage.vue')
    },
    {
      path: '/payment/:classroom_id',
      name: 'Payment',
      component: () => import('@/views/PaymentPage.vue')
    },
    {
      path: '/paysuccess',
      name: 'Paysuccess',
      component: () => import('@/views/PaySuccessfulPage.vue')
    },
    {
      path: '/message',
      name: 'Message',
      component: () => import('@/views/MessagePage.vue')
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  store.commit('loading/setLoading', true)

  // Check if the route requires authentication
  if (to.matched.some((route) => route.meta.requiresAuth)) {
    // Check if the user is authenticated
    if (window.$cookies.isKey('auth_token')) {
      // Check if the user info is already loaded
      if (store.state.user.user_id === null) {
        store
          .dispatch('user/loadUser')
          .then(() => {
            next()
          })
          .catch(() => {
            next('/login')
          })
      } else {
        next() // User is authenticated, proceed to the route
      }
      // User is authenticated, proceed to the route
      store.commit('loading/setLoading', false)
      next()
    } else {
      // User is not authenticated, redirect to the login page
      next('/login')
    }
  } else {
    // If the route does not require authentication, proceed as usual
    store.commit('loading/setLoading', false)
    next()
  }
})

export default router
