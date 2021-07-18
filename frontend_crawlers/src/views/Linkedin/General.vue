<template>
    <div>
        <card>
            <div class="container">
                <div class="row">
                    <div class="col-4 d-flex align-self-center">
                        <h3>Linkedin actions</h3>
                    </div>
                </div>
            </div>
        </card>

        <card>
            <div class="container mt-4">
                <div class="row">
                    <div class="col d-flex align-self-center">
                        <b-list-group>
                            <b-list-group-item href="/linkedin/profile"
                                >Get profile info (comming
                                soon)</b-list-group-item
                            >
                            <b-list-group-item href="/linkedin/sn/profile"
                                >Get Sales Navigator profile info (comming
                                soon)</b-list-group-item
                            >
                            <b-list-group-item href="/linkedin/search"
                                >Search</b-list-group-item
                            >
                            <b-list-group-item href="/linkedin/search/scribe"
                                >Search detailed</b-list-group-item
                            >
                            <b-list-group-item href="/linkedin/sn/search"
                                >Search SN</b-list-group-item
                            >
                            <b-list-group-item href="/linkedin/sn/search/scribe"
                                >Search SN detailed</b-list-group-item
                            >
                            <b-list-group-item href="/linkedin/post"
                                >Get info from post - likes, comments, etc
                                (comming soon)</b-list-group-item
                            >
                        </b-list-group>
                    </div>
                </div>
            </div>
        </card>
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
