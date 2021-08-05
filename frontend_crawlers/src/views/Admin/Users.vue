<template>
    <div>
        <b-container>
            <b-row>
                <b-col md="4" class="d-flex align-self-center">
                    <p class="title">Users</p>
                </b-col>
                <b-col md="8" class="d-flex flex-row-reverse align-self-center">
                    <b-button @click.prevent="refresh" variant="outline-primary"
                        >Refresh</b-button
                    >
                </b-col>
            </b-row>
        </b-container>

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
                        :items="users"
                    >
                    </b-table>
                </b-col>
                <b-col md="2" v-else class="d-flex align-self-center mt-5">
                    <b-spinner variant="primary" label="Spinning"></b-spinner>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>
<script>
import axios from "@/api/axios-auth"

const USERS_API = "/users"

export default {
    data() {
        return {
            loaded: false,

            users: [],
        }
    },
    methods: {
        makeToast(variant = null, text) {
            this.$bvToast.toast(text, {
                title: `${variant || "info"}`,
                variant: variant,
                solid: true,
            })
        },
        async loadUsers() {
            try {
                let res = await axios.get(USERS_API)
                let r = res.data
                if (r.code < 0) {
                    console.log(r)
                    this.makeToast("danger", "Can't load users. Server error.")
                } else {
                    this.users = JSON.parse(r.data)
                    console.log("users: ", this.users)
                }
            } catch (error) {
                let msg = "Error loading users. ERROR: " + error
                console.error(msg, error.stack)
                this.makeToast("danger", "Can't load users")
            }

            this.loaded = true
        },
        async refresh() {
            try {
                this.loaded = false
                await this.loadUsers()
                this.makeToast("success", "Refreshed")
            } catch (err) {
                console.log(err)
            }
        },
    },
    async mounted() {
        await this.loadUsers()
    },
    created() {},
}
</script>
<style>
.title {
    font-size: 32px;
    line-height: 65px;
    font-weight: bold;
    color: #0373b2;
}
.text {
    color: #0373b2;
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
