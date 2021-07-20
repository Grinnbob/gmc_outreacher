import axios from "axios"
import router from "../../router/index"

const LOGIN_PATH = "/auth"
const REGISTER_PATH = "/user/create"

const axios_instance = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
})

const state = {
    login: null,
    token: null,
    role: null,
    login_error: "",
    register_error: "",
}

const mutations = {
    auth_user(state, user_data) {
        state.login = user_data.login
        state.token = user_data.token
        state.user_id = user_data.user_id

        state.login_error = ""
        state.register_error = ""
    },
    clear_auth_data(state) {
        state.login = null
        state.token = null
        state.user_id = null

        state.login_error = ""
        state.register_error = ""
    },
    put_login_error(state, error) {
        state.login_error = error
    },
    put_register_error(state, error) {
        state.register_error = error
    },
}

const getters = {
    isAuthenticated(state) {
        return state.token !== null
    },
    getLoginError(state) {
        return state.login_error
    },
    getRegisterError(state) {
        return state.register_error
    },
}

const actions = {
    login: ({ commit }, auth_data) => {
        return new Promise((resolve, reject) => {
            commit("clear_auth_data")

            axios_instance
                .post(LOGIN_PATH, {
                    login: auth_data.login,
                    password: auth_data.password,
                })
                .then((response) => {
                    let r = response.data

                    if (r.code == 0) {
                        commit("auth_user", {
                            login: auth_data.login,
                            token: r.data.token,
                        })
                        localStorage.setItem("token", r.data.token)
                        localStorage.setItem("login", r.data.login)
                        //localStorage.setItem("role", r.data.role)
                        localStorage.setItem("user_id", r.data._id)

                        console.log("r: ", r)
                        resolve(r)
                    } else {
                        commit("put_login_error", r.msg)
                        reject(r.msg)
                    }
                })
                .catch((error) => {
                    commit("put_login_error", error)
                    reject(error)
                })
        })
    },
    register: ({ commit }, auth_data) => {
        return new Promise((resolve, reject) => {
            commit("clear_auth_data")

            axios_instance
                .post(REGISTER_PATH, {
                    login: auth_data.login,
                    password: auth_data.password,
                })
                .then((response) => {
                    let r = response.data

                    if (r.code == 0) {
                        commit("auth_user", {
                            login: auth_data.login,
                            token: r.data.token,
                        })
                        localStorage.setItem("token", r.data.token)
                        localStorage.setItem("login", r.data.login)
                        //localStorage.setItem("role", r.data.role)
                        localStorage.setItem("user_id", r.data._id)

                        resolve(r)
                    } else {
                        commit("put_register_error", r.msg)
                        //console.log("put_register_error r:", r)
                        reject(r.msg)
                    }
                })
                .catch((error) => {
                    commit("put_register_error", error)
                    //console.log("put_register_error catch error:", error)
                    reject(error)
                })
        })
    },

    autoLogin({ commit }) {
        return new Promise((resolve, reject) => {
            let token = localStorage.getItem("token")
            let login = localStorage.getItem("login")

            if (!token || !login) {
                reject()
                return
            }

            commit("auth_user", { login: login, token: token })
            resolve()
        })
    },
    logout: ({ commit }) => {
        return new Promise((resolve, reject) => {
            commit("clear_auth_data")
            localStorage.removeItem("login")
            localStorage.removeItem("token")
            router.push("login")
            resolve()
        })
    },
}

export default {
    namespaced: true,
    state,
    mutations,
    getters,
    actions,
}
