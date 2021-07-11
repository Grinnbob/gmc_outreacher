import axios from "axios"
import router from "../../router/index"

axios.create({
    baseURL: process.env.VUE_APP_API_URL,
})

const state = {
    email: null,
    token: null,
    role: null,
    login_error: "",
    register_error: "",
}

const mutations = {
    auth_user(state, user_data) {
        state.email = user_data.email
        state.token = user_data.token
        state.user_id = user_data.user_id

        state.login_error = ""
        state.register_error = ""
    },
    clear_auth_data(state) {
        state.email = null
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

            const login_path = "/sign_in"
            var login_data = new FormData()
            login_data.append("_auth_data", JSON.stringify(auth_data))

            axios
                .post(login_path, login_data)
                .then((response) => {
                    let r = response.data

                    if (r.code == 1) {
                        commit("auth_user", {
                            email: auth_data.email,
                            token: r.token,
                        })
                        localStorage.setItem("token", r.token)
                        localStorage.setItem("email", r.email)
                        localStorage.setItem("role", r.role)
                        localStorage.setItem("user_id", r.user_id)

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

            const register_path = "/sign_up"
            var register_data = new FormData()
            register_data.append("_auth_data", JSON.stringify(auth_data))

            axios
                .post(register_path, register_data)
                .then((response) => {
                    let r = response.data

                    if (r.code == 1) {
                        commit("auth_user", {
                            email: auth_data.email,
                            token: r.token,
                        })
                        localStorage.setItem("token", r.token)
                        localStorage.setItem("email", r.email)
                        localStorage.setItem("role", r.role)
                        localStorage.setItem("user_id", r.user_id)

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
            let email = localStorage.getItem("email")

            if (!token || !email) {
                reject()
                return
            }

            commit("auth_user", { email: email, token: token })
            resolve()
        })
    },
    logout: ({ commit }) => {
        return new Promise((resolve, reject) => {
            commit("clear_auth_data")
            localStorage.removeItem("email")
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
