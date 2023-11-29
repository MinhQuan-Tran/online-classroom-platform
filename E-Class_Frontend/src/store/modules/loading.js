// initial state
const state = () => ({
  loading: true
})

// getters
const getters = {}

// actions
const actions = {}

// mutations
const mutations = {
  setLoading(state, loading) {
    state.loading = loading
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
