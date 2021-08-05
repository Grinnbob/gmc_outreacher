<template>
    <div>
        <b-container class="mt-4">
            <b-row>
                <b-col>
                    <p class="text-center llama_title">
                        Linkedin Sales Navigator actions
                    </p>

                    <div class="card-deck justify-content-md-center">
                        <!-- <a href="/linkedin/sn/search">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        Scribe search SN
                                    </p>
                                    <p class="card-text card_text">
                                        Get profiles with info from Sales
                                        Navigator search.
                                    </p>
                                </div>
                            </div>
                        </a> -->

                        <a href="/linkedin/sn/search/scribe">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        Scribe search SN detailed
                                    </p>
                                    <p class="card-text card_text">
                                        Get profiles with detailed info from
                                        Sales Navigator search.
                                    </p>
                                </div>
                            </div>
                        </a>

                        <a href="/linkedin/sn/scribe">
                            <div
                                class="card mr-3 mb-3"
                                style="width: 18rem; height: 11rem;"
                            >
                                <div class="card-body text-center mx-4 my-4">
                                    <p class="card-text card_title">
                                        One profile scribe
                                    </p>
                                    <p class="card-text card_text">
                                        Get info from exec Sales Navigator
                                        profile
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
