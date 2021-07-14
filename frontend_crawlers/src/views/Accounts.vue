<template>
    <div>
        <card>
            <div class="container">
                <div class="row">
                    <div class="col-4 d-flex align-self-center">
                        <h3><i class="nc-icon nc-circle-09"></i> Accounts</h3>
                    </div>
                    <div
                        class="col-8 d-flex flex-row-reverse align-self-center"
                    >
                        <b-button
                            @click.prevent="onAddAccount"
                            variant="outline-primary"
                            >Add account</b-button
                        >
                    </div>
                </div>
            </div>
        </card>

        <card>
            <div class="container mt-4">
                <div class="row">
                    <div class="col d-flex align-self-center">
                        <b-table
                            striped
                            hover
                            fixed
                            :items="account_data.map(accountsMapping)"
                        ></b-table>
                    </div>
                </div>
            </div>
        </card>
    </div>
</template>
<script>
import axios from "@/api/axios-auth"

const ACCOUNTS_API = "/accounts"

export default {
    data() {
        return {
            account_data: [],
        }
    },
    computed: {},
    methods: {
        accountsMapping(el) {
            let new_el = {}
            new_el.type = "linkedin"
            if (el.login) new_el.login = el.login
            if (el.cookies && el.cookies.length > 0)
                new_el.li_at = el.cookies.find((c) => c.name === "li_at").value

            return new_el
        },
        async onAddAccount() {
            this.$router.push({ path: "/account/add" })
        },
        async loadAccounts() {
            try {
                let res = await axios.post(ACCOUNTS_API, {})
                let r = res.data
                if (r.code < 0) {
                    let msg = "Error loading accounts." + r.msg
                    console.log(msg)
                } else {
                    this.account_data = r.data
                    console.log("accounts: ", this.account_data)
                }
            } catch (error) {
                let msg = "Error loading accounts. ERROR: " + error
                console.error(msg, error.stack)
            }
        },
    },
    async mounted() {
        await this.loadAccounts()
        //console.log(this.account_data)
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
