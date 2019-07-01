import axios from 'axios'
import apiConfig from './apiConfig'
import auth from '@/services/auth'

const api = axios.create(apiConfig)

api.interceptors.request.use(
  requestConfig => {
    if (!requestConfig.hasPermission) {
      requestConfig.headers = {
        ...requestConfig.headers,
        ...auth.getAuthHeader()
      }
    }
    requestConfig.url = `${requestConfig.baseURL}${requestConfig.url}`
    return requestConfig
  },
  error => Promise.reject(error)
)

// Add a response interceptor
api.interceptors.response.use(
  res => {
    let response = res.data
    let error
    if (response.error) {
      error = response.error || {}
      response = {
        error: {
          status: 'ERROR',
          code: error.errorCode || 'Unknown',
          message: error.description || 'Unknown Error'
        }
      }
    }

    return response
  },
  error => {
    let err = error.response || {}
    let code = err.status
    let message
    let status = 'ERROR'
    let errorObj
    if (err.status === 401) {
      if (!!err.data && !!err.data.detail) {
        if (err.data.detail === 'Signature has expired.') {
          auth.logout()
        }
        message = err.data.detail
      } else {
        message = 'Unauthorized'
      }
    } else if (!!err.data && !!err.data.message) {
      message = err.data.message
    } else if (err.status === 404) {
      message = 'Item not found'
    } else {
      message =
        'Unexpected error occurred. Please contact system administrator.'
    }
    errorObj = {
      status,
      code,
      message
    }

    return Promise.reject(errorObj)
  }
)

export default api
