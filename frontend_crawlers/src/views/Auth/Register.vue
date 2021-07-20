<template>
    <auth-layout pageClass="login-page">
        <b-row class="d-flex justify-content-center align-items-center">
            <b-col class="col-lg-4 col-md-6 col-sm-8">
                <form method="#" action="#">
                    <!--You can specify transitions on initial render. The `card-hidden` class will be present initially and then it will be removed-->
                    <card>
                        <div slot="header">
                            <h3 class="card-title text-center">Register</h3>
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
                                    placeholder="Enter password"
                                ></b-form-input>
                            </b-form-group>

                            <b-form-group
                                label="Repeat password"
                                label-for="repeat-password-input"
                                class="my-3"
                            >
                                <b-form-input
                                    id="repeat-password-input"
                                    v-model="model.repeat_password"
                                    placeholder="Password"
                                ></b-form-input>
                            </b-form-group>

                            <div v-if="error" class="form-group my-3">
                                <small class="text-danger">{{ error }}</small>
                            </div>
                        </div>

                        <div class="text-center">
                            <b-button
                                class="my-3"
                                :disabled="loading"
                                @click.prevent="onSubmit"
                                variant="outline-primary"
                                >Create Account</b-button
                            >
                        </div>

                        <p class="policy_text">
                            By clicking the "Create Account" button, I expressly
                            agree to the Llama
                            <a
                                href="https://outreacher24.com/terms-and-conditions"
                                target="_blank"
                                >Terms of Use</a
                            >
                            and understand that my account information will be
                            used according to Llama
                            <a
                                href="https://outreacher24.com/privacy-policy"
                                target="_blank"
                                >Privacy Policy</a
                            >
                        </p>
                    </card>
                </form>
            </b-col>
        </b-row>
    </auth-layout>
</template>
<script>
import { mapGetters } from "vuex"

export default {
    components: {},
    computed: {
        ...mapGetters("auth", {
            error: "getRegisterError",
            isAuth: "isAuthenticated",
        }),
    },

    data() {
        return {
            loading: false,
            //color: "#a7a7ff",

            model: {
                login: "",
                password: "",
                repeat_password: "",
            },
        }
    },
    methods: {
        async onSubmit() {
            if (
                !this.model.login ||
                !this.model.password ||
                !this.model.repeat_password
            ) {
                console.log("Empty input")
                //this.error = "Empty input"
                return
            }

            if (this.model.password !== this.model.repeat_password) {
                console.log("Password mismatch")
                //this.error = "Password mismatch"
                return
            }

            var _this = this
            this.loading = true

            await this.$store
                .dispatch("auth/register", this.model)
                .then(
                    (resolve) => {
                        _this.$router.push("profile")
                        _this.loading = false
                    },
                    (reject) => {
                        console.log("error here: ", reject)
                        _this.loading = false
                    }
                )
                .catch((err) => {
                    console.error("register error: ", err)
                    _this.loading = false
                })
        },
    },
    beforeDestroy() {},
}
</script>
<style>
.navbar-nav .nav-item p {
    line-height: inherit;
    margin-left: 5px;
}
.policy_text {
    font-size: 10px;
    color: grey;
}
</style>
