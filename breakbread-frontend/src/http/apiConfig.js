import { API_BASE_URL } from '@/constants'
const apiConfig = {
  baseURL: API_BASE_URL,
  transformRequest: [
    function (data, headers) {
      // Do whatever you want to transform the data

      return data
    }
  ],

  transformResponse: [
    function (data) {
      // Do whatever you want to transform the data

      return data
    }
  ],

  // `headers` are custom headers to be sent
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
  },

  // flag to check whether to send auth token or not
  hasPermission: false,
  // `paramsSerializer` is an optional function in charge of serializing `params`
  // paramsSerializer: function(params) {
  //   return params;
  // },

  // `withCredentials` indicates whether or not cross-site Access-Control requestsshould be made using credentials
  withCredentials: false,

  // `auth` indicates that HTTP Basic auth should be used, and supplies credentials.
  // This will set an `Authorization` header, overwriting any existing
  // `Authorization` custom headers you have set using `headers`.
  // auth: {
  //   username: "janedoe",
  //   password: "s00pers3cret"
  // },

  // `responseType` indicates the type of data that the server will respond with
  // options are: 'arraybuffer', 'document', 'json', 'text', 'stream'
  //   browser only: 'blob'
  responseType: 'json', // default

  // `responseEncoding` indicates encoding to use for decoding responses
  // Note: Ignored for `responseType` of 'stream' or client-side requests
  responseEncoding: 'utf8' // default
}
export default apiConfig
