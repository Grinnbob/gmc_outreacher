import axios from "axios"
import store from "../store/index"

const instance = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    headers: {
        "Content-Type": "application/json",
        // Authorization: {
        //     toString() {
        //         return `Bearer ${localStorage.getItem("token")}`
        //     },
        // },
    },
})

// todo remove it
instance.interceptors.request.use(function(request) {
    request.data.login = "servicelogin@gsuit.com"
    request.data.password = "mypass1234"
    return request
})

instance.interceptors.response.use(
    function(response) {
        // Do something with response data
        return response
    },
    function(error) {
        // Do something with response error
        let msg = error.toString()
        if (msg.includes("403")) {
            //console.log('....', localStorage.getItem('token'))

            store
                .dispatch("auth/logout")
                .then(
                    (resolve) => {
                        //_this.$router.push("login");
                    },
                    (reject) => {
                        console.log("error here: ", reject)
                    }
                )
                .catch((err) => {
                    console.error("login error: ", err)
                })
            //router.push("login");
            console.log(`Error: 403 here`)
        }
        return Promise.reject(error)
    }
)

export default instance