<template>
    <auth-layout pageClass="login-page">
        <div class="row d-flex justify-content-center align-items-center">
            <div class="col-lg-4 col-md-6 col-sm-8">
                <form method="#" action="#">
                    <!--You can specify transitions on initial render. The `card-hidden` class will be present initially and then it will be removed-->
                    <card>
                        <div slot="header">
                            <h3 class="card-title text-center">Login</h3>
                        </div>

                        <b-container>
                            <b-row class="justify-content-md-center">
                                <b-col
                                    md="2"
                                    v-if="loading"
                                    class="d-flex align-self-center mt-5"
                                >
                                    <b-spinner
                                        variant="primary"
                                        label="Spinning"
                                    ></b-spinner>
                                </b-col>
                            </b-row>
                        </b-container>

                        <div v-if="!loading">
                            <b-form-group
                                label="Email address"
                                label-for="email-input"
                                class="my-3"
                            >
                                <b-form-input
                                    id="email-input"
                                    v-model="model.login"
                                    :state="login_state"
                                    placeholder="Enter email"
                                ></b-form-input>
                            </b-form-group>

                            <b-form-group
                                label="Password"
                                label-for="password-input"
                                class="my-3"
                            >
                                <b-form-input
                                    id="password-input"
                                    v-model="model.password"
                                    :state="password_state"
                                    placeholder="Enter password"
                                ></b-form-input>
                            </b-form-group>

                            <div v-if="error" class="form-group">
                                <small class="text-danger">{{ error }}</small>
                            </div>
                        </div>

                        <div class="text-center">
                            <b-button
                                class="my-3"
                                :disabled="loading"
                                @click.prevent="onSubmit"
                                variant="outline-primary"
                                >Login</b-button
                            >
                        </div>
                    </card>
                </form>
            </div>
        </div>
    </auth-layout>
</template>
<script>
import { mapGetters } from "vuex"

export default {
    components: {},
    computed: {
        ...mapGetters("auth", {
            error: "getLoginError",
            isAuth: "isAuthenticated",
        }),
    },
    data() {
        return {
            loading: false,
            //color: "#a7a7ff",

            login_state: null,
            password_state: null,

            model: {
                login: "",
                password: "",
            },
        }
    },
    methods: {
        toggleNavbar() {
            document.body.classList.toggle("nav-open")
        },
        closeMenu() {
            document.body.classList.remove("nav-open")
            document.body.classList.remove("off-canvas-sidebar")
        },
        onSubmit() {
            if (!this.model.login) {
                this.login_state = false
                console.log("Empty input")
                //this.error = "Empty input"
                return
            }

            this.login_state = true

            if (!this.model.password) {
                this.password_state = false
                console.log("Empty input")
                //this.error = "Empty input"
                return
            }

            this.password_state = true

            var _this = this
            this.loading = true

            this.$store
                .dispatch("auth/login", this.model)
                .then(
                    (resolve) => {
                        _this.$router.push("guide")
                        _this.loading = false
                    },
                    (reject) => {
                        console.log("error here: ", reject)
                        _this.loading = false
                        _this.password_state = false
                        _this.login_state = false
                    }
                )
                .catch((err) => {
                    console.error("login error: ", err)
                    _this.loading = false
                    _this.password_state = false
                    _this.login_state = false
                })
        },
    },
    beforeDestroy() {
        this.closeMenu()
    },
}
</script>
<style>
.navbar-nav .nav-item p {
    line-height: inherit;
    margin-left: 5px;
}
.text {
    display: flex;
    font-size: 12px;
    font-weight: 200;
    line-height: 30px;
    text-transform: uppercase;
    color: rgb(119, 119, 119);
}
</style>
