import axios from 'axios'

import { BASE_URL } from '@/constants'
import router from '@/main'

// URL and endpoint constants
const API_URL = BASE_URL
const LOGIN_URL = API_URL + 'api-token-auth/'
const SIGNUP_URL = API_URL + 'api/signup/'

export default {
  // User object will let us check authentication status
  user: {
    authenticated: false
  },

  // Send a request to the login URL and save the returned JWT
  login (creds) {
    return new Promise((resolve, reject) => {
      axios.post(LOGIN_URL, creds).then(
        res => {
          var data = res.data
          if (data.error) {
            reject(data.error)
          } else {
            const { token, user } = data
            localStorage.setItem('access_token', token)
            localStorage.setItem('email', user.email)
            localStorage.setItem('username', user.first_name)
            localStorage.setItem('is_admin', user.is_superuser)
            this.user.authenticated = true
            resolve(data)
          }
        },
        error => {
          reject(error)
        }
      )
    })
  },

  signup (creds) {
    return new Promise((resolve, reject) => {
      axios.post(SIGNUP_URL, creds).then(
        res => {
          var data = res.data
          if (data.error) {
            reject(data.error)
          } else {
            localStorage.setItem('access_token', data.access)
            localStorage.setItem('refresh_token', data.refresh)
            this.user.authenticated = true
            resolve(data)
          }
        },
        error => {
          reject(error)
        }
      )
    })
  },

  // To log out, we just need to remove the token
  logout () {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('email')
    localStorage.removeItem('username')
    localStorage.removeItem('is_admin')
    this.user.authenticated = false
    router.push('/login')
  },
  getUserInfo () {
    if (localStorage.getItem('access_token')) {
      return {
        refresh_token: localStorage.getItem('refresh_token'),
        email: localStorage.getItem('email'),
        username: localStorage.getItem('username'),
        is_admin: localStorage.getItem('is_admin')
      }
    } else {
      this.user.authenticated = false
    }
  },
  checkAuth () {
    var jwt = localStorage.getItem('access_token')
    if (jwt) {
      this.user.authenticated = true
    } else {
      this.user.authenticated = false
    }
  },

  // The object to be passed as a header for authenticated requests
  getAuthHeader () {
    return {
      Authorization: 'JWT ' + localStorage.getItem('access_token')
    }
  }
}
