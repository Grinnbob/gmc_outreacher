<template>
    <div>
        <b-container class="mt-4">
            <b-row>
                <b-col>
                    <p class="text-center title">
                        Basic Linkedin actions
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

                        <a href="/linkedin/search/scribe">
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
                                        basic Linkedin search.
                                    </p>
                                </div>
                            </div>
                        </a>

                        <a href="/linkedin/scribe">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        One profile scribe
                                    </p>
                                    <p class="card-text card_text">
                                        Get info from exec profile
                                    </p>
                                </div>
                            </div>
                        </a>

                        <a href="/linkedin/post">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        Post info scribe
                                    </p>
                                    <p class="card-text card_text">
                                        Get info from post - likes, comments,
                                        etc.
                                    </p>
                                    <p style="color: red;">coming soon</p>
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
<style>
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
