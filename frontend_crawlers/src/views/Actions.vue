<template>
    <div>
        <card>
            <div class="container">
                <div class="row">
                    <div class="col-4 d-flex align-self-center">
                        <h3>Actions</h3>
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
                            :items="actions_data.map(actionsMapping)"
                        ></b-table>
                    </div>
                </div>
            </div>
        </card>
    </div>
</template>
<script>
import axios from "@/api/axios-auth"

const ACCOUNTS_API = "/actions"

export default {
    data() {
        return {
            actions_data: [],
            action_codes: {
                linkedin_check_reply: { id: 1, name: "Check reply" },
                linkedin_connect: { id: 2, name: "Connect" },
                linkedin_send_message: { id: 3, name: "Send message" },
                linkedin_check_accept: { id: 4, name: "Check aaccept" },
                linkedin_search: { id: 5, name: "Search" },
                linkedin_parse_profile: { id: 6, name: "Parse profile" },
                linkedin_visit_profile: { id: 7, name: "Visit profile" },
                linkedin_search_sn: { id: 8, name: "Search Sales Navigator" },
                linkedin_parse_profile_sn: {
                    id: 9,
                    name: "Parse profile Sales Navigator",
                },
                linkedin_post_parsing: { id: 10, name: "Post parsing" },
                linkedin_search_scribe: { id: 11, name: "Search and scribe" },
                linkedin_search_scribe_sn: {
                    id: 12,
                    name: "Search and scribe Sales Navigator",
                },
            },
        }
    },
    computed: {},
    methods: {
        actionsMapping(el) {
            let new_el = {}
            try {
                new_el.action = Object.values(this.action_codes).find(
                    (action) => action.id === el.action
                ).name
            } catch (err) {
                console.log("action not found: ", err)
                new_el.action = "unknown"
            }

            new_el.status = el.status === 0 ? "In progress" : "Completed"
            new_el.input = el.input_data

            try {
                new_el.result = JSON.parse(el.result_data.data)
            } catch (err) {
                new_el.result = el.result_data.data
            }

            new_el.date = el.timestamp

            return new_el
        },
        async loadActions() {
            try {
                let res = await axios.post(ACCOUNTS_API, {})
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
