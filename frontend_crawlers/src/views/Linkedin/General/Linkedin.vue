<template>
    <div>
        <b-container class="mt-4">
            <b-row>
                <b-col>
                    <p class="text-center llama_title">
                        Basic LinkedIn actions
                    </p>

                    <div class="card-deck justify-content-md-center">
                        <!-- <a href="/linkedin/search">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        Scribe search
                                    </p>
                                    <p class="card-text card_text">
                                        Get profiles with info from basic
                                        Linkedin search
                                    </p>
                                </div>
                            </div>
                        </a> -->

                        <a @click="$router.push('/linkedin/search/scribe')">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        Scribe search detailed
                                    </p>
                                    <p class="card-text card_text">
                                        Get profiles with detailed info from
                                        basic LinkedIn searches.
                                    </p>
                                </div>
                            </div>
                        </a>

                        <a @click="$router.push('/linkedin/scribe')">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        One profile scribe
                                    </p>
                                    <p class="card-text card_text">
                                        Get info from exec profiles
                                    </p>
                                </div>
                            </div>
                        </a>

                        <a @click="$router.push('/linkedin/post')">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        Post info scribe
                                    </p>
                                    <p class="card-text card_text">
                                        Get info from posts - likes, comments,
                                        etc.
                                    </p>
                                    <p style="color: red;">Coming soon</p>
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
