<template>
    <div>
        <card>
            <div class="container">
                <div class="row">
                    <div class="col-4 d-flex align-self-center">
                        <h3>Accounts</h3>
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

const ACCTIONS_API = "/actions"

export default {
    data() {
        return {
            actions_data: [],
        }
    },
    computed: {},
    methods: {
        accountsMapping(el) {},
        async onAddAccount() {
            this.$router.push({ path: "/account/add" })
        },
        async loadActions() {
            try {
                let res = await axios.post(ACCTIONS_API, {
                    input_data: { action: 6 },
                })
                let r = res.data
                if (r.code < 0) {
                    let msg = "Error loading actions." + r.msg
                    console.log(msg)
                } else {
                    this.actions_data = r.data
                    console.log("actions: ", this.actions_data)
                }
            } catch (error) {
                let msg = "Error loading actions. ERROR: " + error
                console.error(msg, error.stack)
            }
        },
    },
    async mounted() {
        await this.loadActions()
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
