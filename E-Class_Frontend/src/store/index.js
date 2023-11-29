import { createStore } from 'vuex'
import user from './modules/user'
import loading from './modules/loading'

export default createStore({
  modules: {
    user,
    loading
  }
})
