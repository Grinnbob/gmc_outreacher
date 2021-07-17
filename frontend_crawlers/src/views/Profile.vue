<template>
    <div>
        <card>
            <div class="container">
                <div class="row">
                    <div class="col-4 d-flex align-self-center">
                        <h3><i class="nc-icon nc-circle-09"></i> Profile</h3>
                    </div>
                    <div
                        class="col-8 d-flex flex-row-reverse align-self-center"
                    >
                        <!-- <button
                            @click.prevent="change_password"
                            type="button"
                            class="btn btn-default btn-success mx-1"
                        >
                            Change password
                        </button> -->
                        <b-button
                            @click.prevent="onLogout"
                            variant="outline-primary"
                            >Add profile</b-button
                        >
                    </div>
                </div>
            </div>
        </card>

        <card>
            <card>
                <p class="info">E-mail</p>
                <p>{{ user_data.login }}</p>
                <div v-if="user_data.role == 'admin'">
                    <p class="info">Role</p>
                    <p>{{ user_data.role }}</p>
                </div>
            </card>
        </card>
    </div>
</template>
<script>
import axios from "@/api/axios-auth"
const PROFILE_API = "/user"

export default {
    data() {
        return {
            user_data: {},
        }
    },
    methods: {
        onLogout() {
            var _this = this
            this.$store
                .dispatch("auth/logout")
                .then(
                    (resolve) => {
                        _this.$router.push("login")
                    },
                    (reject) => {
                        console.log("error here: ", reject)
                    }
                )
                .catch((err) => {
                    console.error("login error: ", err)
                })
        },
        async loadUser() {
            try {
                let res = await axios.post(PROFILE_API, {})
                let r = res.data
                if (r.code < 0) {
                    let msg = "Error loading user." + r.msg
                    console.log(msg)
                } else {
                    this.user_data = JSON.parse(r.user)
                    console.log("user: ", this.user_data)
                }
            } catch (error) {
                let msg = "Error loading user. ERROR: " + error
                console.error(msg, error.stack)
            }
        },
    },
    async mounted() {
        await this.loadUser()
        //console.log(this.user_data)
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
