import axios from 'axios'

export function authRequired (to, from, next) {
  if (User.isAuthenticated()) {
    next()
  } else {
    next({
      path: '/'
    })
  }
}

export const API = 'http://localhost:8000/api'

export const User = {
  get () {
    try {
      /**
       * @property {String} email
       * @property {String} tracking_id
       * @property {String} token
       */
      return JSON.parse(localStorage.user)
    } catch (error) {
      return undefined
    }
  },
  set (user) {
    /**
     * @property {String} email
     * @property {String} tracking_id
     * @property {String} token
     */
    localStorage.user = JSON.stringify(user)
  },
  clear () {
    User.set(undefined)
  },
  isAuthenticated () {
    return User.get() !== undefined
  },
  register (email, password) {
    return axios({
      method: 'POST',
      url: API + '/auth/register/',
      data: {
        email: email,
        password: password
      },
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(result => {
      return result.data
    }).catch(error => {
      console.error(error)
    })
  },
  login (email, password) {
    return axios({
      method: 'POST',
      url: API + '/auth/login/',
      data: {
        email: email,
        password: password
      },
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(result => {
      User.set(result.data)
      return User.get()
    }).catch(error => {
      console.error(error)
    })
  },
  logout () {
    return axios({
      method: 'POST',
      url: API + '/auth/logout/',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + User.get().token
      }
    }).then(result => {
      User.clear()
      return result.data
    }).catch(error => {
      console.error(error)
    })
  }
}

export const Analytics = {
  consolidated () {
    return axios({
      method: 'GET',
      url: API + '/analytics/consolidated/',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + User.get().token
      }
    }).then(result => {
      return result.data
    }).catch(error => {
      console.error(error)
    })
  },
  topPages () {
    return axios({
      method: 'GET',
      url: API + '/analytics/top/pages/',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + User.get().token
      }
    }).then(result => {
      return result.data.pages
    }).catch(error => {
      console.error(error)
    })
  },
  topCountries () {
    return axios({
      method: 'GET',
      url: API + '/analytics/top/countries/',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + User.get().token
      }
    }).then(result => {
      return result.data.countries
    }).catch(error => {
      console.error(error)
    })
  },
  topBrowsers () {
    return axios({
      method: 'GET',
      url: API + '/analytics/top/browsers/',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + User.get().token
      }
    }).then(result => {
      return result.data.browsers
    }).catch(error => {
      console.error(error)
    })
  },
  topScreenResolutions () {
    return axios({
      method: 'GET',
      url: API + '/analytics/top/screen_resolutions/',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + User.get().token
      }
    }).then(result => {
      return result.data.screen_resolutions
    }).catch(error => {
      console.error(error)
    })
  }
}
