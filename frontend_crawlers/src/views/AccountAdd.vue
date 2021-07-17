<template>
    <div>
        <card>
            <div class="container">
                <div class="row">
                    <div class="col-4 d-flex align-self-center">
                        <h3>
                            Add account
                        </h3>
                    </div>
                </div>
            </div>
        </card>

        <card>
            <div class="container">
                <b-row class="my-1">
                    <b-col sm="8">
                        <p>
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
                            placeholder="Enter your login"
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
                            placeholder="Enter your li_at cookie value"
                        ></b-form-input>
                    </b-col>
                </b-row>
                <b-row class="my-4">
                    <b-col sm="2"> </b-col>
                    <b-col sm="10">
                        <b-button
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
            login: "",
            password: "",
            li_at: "",
        }
    },
    computed: {},
    methods: {
        async onAddAccount() {
            try {
                if (this.login == "") {
                    console.log("empty login")
                    return
                }

                if (this.li_at == "") {
                    console.log("empty li_at")
                    return
                }

                let res = await axios.post(ACCOUNTS_API, {
                    input_data: { li_at: this.li_at, login: this.login },
                })
                let r = res.data
                if (r.code < 0) {
                    let msg = "Error loading accounts." + r.msg
                    console.log(msg)
                } else {
                    console.log("account added - success!")
                }
            } catch (error) {
                let msg = "Error loading accounts. ERROR: " + error
                console.error(msg, error.stack)
            }
        },
    },
    async mounted() {},
    created() {},
}
</script>
<style>
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
