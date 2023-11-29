// initial state
const state = () => ({
  user_id: null,
  username: null,
  email: null,
  phone_number: null,
  user_type: null
})

// getters
const getters = {
  getUserId: (state) => state.user_id,
  getUsername: (state) => state.username,
  getEmail: (state) => state.email,
  getPhoneNumber: (state) => state.phone_number,
  getUserType: (state) => state.user_type
}

// actions
const actions = {
  loadUser({ commit }) {
    return new Promise((resolve, reject) => {
      fetch(`${import.meta.env.VITE_ROOT_API}/users/me`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.$cookies.get('csrftoken'),
          Authorization: window.$cookies.get('auth_token')
        }
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((data) => {
              throw new Error(data.message)
            })
          }
          return response.json()
        })
        .then((data) => {
          commit('setUser', data.user)
          resolve(data)
        })
        .catch((error) => {
          console.error(error)
          window.$cookies.remove('auth_token')
          reject(error)
        })
    })
  }
}

// mutations
const mutations = {
  setUser(state, user) {
    // console.log("Received user object:", user);
    // console.log('Before mutation state:', { ...state })
    state.user_id = user.user_id
    state.username = user.username
    state.email = user.email
    state.phone_number = user.phone_number
    state.user_type = user.user_type
    // console.log('After mutation state:', { ...state })
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
