<template>
    <div>
        <card>
            <b-container>
                <b-row>
                    <b-col class="col-4 d-flex align-self-center">
                        <h3>Accounts</h3>
                    </b-col>
                    <b-col
                        class="col-8 d-flex flex-row-reverse align-self-center"
                    >
                        <b-button
                            @click.prevent="onAddAccount"
                            variant="outline-primary"
                            >Add account</b-button
                        >
                    </b-col>
                </b-row>
            </b-container>
        </card>

        <card>
            <b-container class="mt-4">
                <b-row class="justify-content-md-center">
                    <b-col v-if="loaded" class="d-flex align-self-center">
                        <b-table
                            responsive
                            striped
                            hover
                            bordered
                            borderless
                            small
                            :items="account_data"
                        ></b-table>
                    </b-col>
                    <b-col md="2" v-else class="d-flex align-self-center mt-5">
                        <b-spinner
                            variant="primary"
                            label="Spinning"
                        ></b-spinner>
                    </b-col>
                </b-row>
            </b-container>
        </card>
    </div>
</template>
<script>
import axios from "@/api/axios-auth"

const ACCOUNTS_API = "/accounts"

export default {
    data() {
        return {
            loaded: false,

            account_data: [],
        }
    },
    computed: {},
    methods: {
        async onAddAccount() {
            this.$router.push({ path: "/account/add" })
        },
        async loadAccounts() {
            try {
                let res = await axios.get(ACCOUNTS_API)
                let r = res.data
                if (r.code < 0) {
                    let msg = "Error loading accounts." + r.msg
                    console.log(msg)
                } else {
                    console.log("accounts: ", r.data)

                    this.account_data = r.data
                        .filter((el) => el.status !== -1)
                        .map((el) => {
                            let new_el = {}
                            new_el.login = el.login
                            new_el.type = el.type === 1 ? "linkedin" : "unknown"
                            new_el.status =
                                el.status === 0
                                    ? "active"
                                    : el.status === 1
                                    ? "blocked"
                                    : "unknown"
                            if (el.cookies && el.cookies.length > 0)
                                new_el.li_at = el.cookies.find(
                                    (c) => c.name === "li_at"
                                ).value

                            return new_el
                        })
                }

                this.loaded = true
            } catch (error) {
                let msg = "Error loading accounts. ERROR: " + error
                console.error(msg, error.stack)
            }
        },
    },
    async mounted() {
        await this.loadAccounts()
    },
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
