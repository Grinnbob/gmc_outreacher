<template>
    <div>
        <card>
            <div class="container">
                <div class="row">
                    <div class="col-4 d-flex align-self-center">
                        <p class="title">
                            Add account
                        </p>
                    </div>
                </div>
            </div>
        </card>

        <card>
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

            <div class="container" v-if="!loading">
                <b-row class="my-1">
                    <b-col sm="8">
                        <p class="text">
                            Enter your linkedin li_at cookie. To get them -
                            download
                            <b-link
                                href="https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/related?hl=en"
                                target="_blank"
                                >chrome extension</b-link
                            >
                            for get cookies and go to your
                            <b-link
                                href="https://www.linkedin.com"
                                target="_blank"
                                >linkedin page</b-link
                            >
                            and extract exactly li_at value and paste here
                        </p>
                    </b-col>
                </b-row>
                <b-row class="my-1">
                    <b-col sm="2">
                        <label for="input-default">Login:</label>
                    </b-col>
                    <b-col sm="6">
                        <b-form-input
                            v-model="login"
                            :state="login_state"
                            placeholder="Enter your Linkedin login"
                        ></b-form-input>
                    </b-col>
                </b-row>
                <!-- <b-row class="my-1">
                    <b-col sm="2">
                        <label for="input-default">Password:</label>
                    </b-col>
                    <b-col sm="6">
                        <b-form-input
                            v-model="password"
                            :state="password_state"
                            placeholder="Enter your password"
                        ></b-form-input>
                    </b-col>
                </b-row> -->
                <b-row class="my-1">
                    <b-col sm="2">
                        <label for="input-default">li_at:</label>
                    </b-col>
                    <b-col sm="6">
                        <b-form-input
                            v-model="li_at"
                            :state="li_at_state"
                            placeholder="Enter your li_at cookie value"
                        ></b-form-input>
                    </b-col>
                </b-row>
                <b-row class="my-4">
                    <b-col sm="2"> </b-col>
                    <b-col sm="10">
                        <b-button
                            :disabled="loading"
                            @click.prevent="onAddAccount"
                            variant="outline-primary"
                            >Add account</b-button
                        >
                    </b-col>
                </b-row>
            </div>
        </card>
    </div>
</template>
<script>
import axios from "@/api/axios-auth"

const ACCOUNTS_API = "/account"

export default {
    data() {
        return {
            loading: false,

            login_state: null,
            li_at_state: null,
            password_state: null,

            login: "",
            password: "",
            li_at: "",
        }
    },
    computed: {},
    methods: {
        makeToast(variant = null, text) {
            this.$bvToast.toast(text, {
                title: `${variant || "info"}`,
                variant: variant,
                solid: true,
            })
        },
        async onAddAccount() {
            try {
                if (!this.login) {
                    this.makeToast("danger", "Empty login")
                    this.login_state = false
                    return
                }

                this.login_state = true

                if (!this.li_at) {
                    this.makeToast("danger", "Empty li_at")
                    this.li_at_state = false
                    return
                }

                this.li_at_state = true

                this.loading = true

                let res = await axios.post(ACCOUNTS_API, {
                    input_data: { li_at: this.li_at, login: this.login },
                })

                let r = res.data
                if (r.code < 0) {
                    let msg = "Error create account." + r.msg
                    this.makeToast("danger", "Can't create account")
                    console.log(msg)
                } else {
                    this.makeToast("success", "Account added ")
                    this.$router.push({ path: "/accounts" })
                }
            } catch (error) {
                let msg = "Error loading accounts. ERROR: " + error
                console.error(msg, error.stack)
                this.makeToast("danger", "Can't create account")
            }

            this.loading = false
        },
    },
    async mounted() {},
    created() {},
}
</script>
<style>
.title {
    font-size: 32px;
    line-height: 65px;
    font-weight: bold;
    color: #262a79;
}
.text {
    color: #262a79;
    font-size: 20px;
}
.card_title {
    text-align: center;
    font-size: 35px;
    font-weight: 500;
}
.info {
    font-size: 20px;
    font-weight: 600;
    height: 10px;
}
</style>
