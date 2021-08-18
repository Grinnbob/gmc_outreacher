<template>
    <div>
        <b-container class="mt-4">
            <b-row>
                <b-col>
                    <p class="text-center llama_title">
                        Choose action type
                    </p>

                    <div class="card-deck justify-content-md-center">
                        <a @click="$router.push('/navigate/linkedin')">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        LinkedIn
                                    </p>
                                    <p class="card-text card_text">
                                        Actions with common LinkedIn account
                                    </p>
                                </div>
                            </div>
                        </a>

                        <a @click="$router.push('/navigate/linkedin/sn')">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        LinkedIn SN
                                    </p>
                                    <p class="card-text card_text">
                                        Actions for accounts with paid Sales
                                        Navigator option
                                    </p>
                                </div>
                            </div>
                        </a>
                    </div>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>
<script>
export default {
    data() {
        return {
            account_data: [],
        }
    },
    computed: {},
    methods: {},
    async mounted() {},
    created() {},
}
</script>
<style scoped>
.llama_title {
    font-size: 32px;
    line-height: 65px;
    font-weight: bold;
    color: #0373b2;
}
.card_text {
    color: #0373b2;
    font-size: 14px;
}
.card_title {
    color: #0373b2;
    font-size: 20px;
    font-weight: bold;
}
</style>
