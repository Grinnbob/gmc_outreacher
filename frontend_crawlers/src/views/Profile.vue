<template>
    <div>
        <card>
            <div class="container">
                <div class="row">
                    <div class="col-4 d-flex align-self-center">
                        <p class="title">Profile</p>
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
                            >Logout</b-button
                        >
                    </div>
                </div>
            </div>
        </card>

        <card>
            <card>
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
export default {
    data() {
        return {
            user_data: {
                login: "",
            },
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
    },
    async mounted() {
        this.user_data.login = localStorage.getItem("login")
    },
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
