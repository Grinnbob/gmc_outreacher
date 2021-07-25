<template>
    <div>
        <card>
            <b-container>
                <b-row>
                    <b-col cols="4" class="d-flex align-self-center">
                        <p class="title">
                            Scribe profile
                        </p>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col cols="6" class="d-flex align-self-center">
                        <p class="text">
                            Get basic Linkedin profile info by link.
                        </p>
                    </b-col>
                </b-row>
            </b-container>
        </card>

        <b-tabs card>
            <b-tab title="Action" active>
                <b-container class="my-5">
                    <b-row>
                        <b-col sm="2">
                            <p class="mb-2">
                                Select account
                                <b-icon
                                    v-b-popover.hover.top="
                                        'Choose your linkedin account'
                                    "
                                    class="ml-2"
                                    icon="exclamation-circle"
                                ></b-icon>
                            </p>
                        </b-col>
                        <b-col sm="6">
                            <b-form-select
                                v-model="selected_account"
                                :options="account_data"
                            ></b-form-select>
                        </b-col>
                    </b-row>
                    <b-row class="my-1">
                        <b-col sm="2">
                            <p class="mb-2">
                                Profile link
                                <b-icon
                                    v-b-popover.hover.top="
                                        'Paste here link to Linkedin profile'
                                    "
                                    class="ml-2"
                                    icon="exclamation-circle"
                                ></b-icon>
                            </p>
                        </b-col>
                        <b-col sm="6">
                            <b-form-input
                                v-model="linkedin"
                                placeholder="https://www.linkedin.com/in/someuser"
                            ></b-form-input>
                        </b-col>
                    </b-row>
                    <b-row class="my-4">
                        <b-col sm="2"> </b-col>
                        <b-col sm="10">
                            <b-button
                                @click.prevent="search"
                                variant="outline-primary"
                                >Start</b-button
                            >
                        </b-col>
                    </b-row>
                </b-container>
            </b-tab>
            <b-tab title="Results">
                <b-container class="mt-4">
                    <b-row>
                        <b-col md="4">
                            <p>
                                <b>Started at:</b>
                                {{
                                    actions_data && actions_data.started_at
                                        ? new Date(actions_data.started_at)
                                        : "-"
                                }}
                            </p>
                        </b-col>
                        <b-col md="4">
                            <p>
                                <b>Finished at:</b>
                                {{
                                    actions_data && actions_data.finished_at
                                        ? new Date(actions_data.finished_at)
                                        : "-"
                                }}
                            </p>
                        </b-col>
                        <b-col
                            md="4"
                            class="d-flex flex-row-reverse align-self-center"
                        >
                            <b-button
                                @click.prevent="exportCSV"
                                variant="outline-primary"
                                >Export CSV</b-button
                            >
                            <b-button
                                @click.prevent="refresh"
                                variant="outline-primary"
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
                                :items="last_result"
                            ></b-table>
                        </b-col>
                        <b-col
                            md="2"
                            v-else
                            class="d-flex align-self-center mt-5"
                        >
                            <b-spinner
                                variant="primary"
                                label="Spinning"
                            ></b-spinner>
                        </b-col>
                    </b-row>
                </b-container>
            </b-tab>
        </b-tabs>
    </div>
</template>
<script>
import axios from "@/api/axios-auth"

const ACCOUNTS_API = "/accounts"
const ACCTION_API = "/action"
const SCRIBE_API = "/scribe"

const ACTION_TYPE = 6

export default {
    data() {
        return {
            loaded: false,

            selected_account: "",
            linkedin: "",

            account_data: [],
            actions_data: {},
            last_result: [],
        }
    },
    computed: {},
    methods: {
        makeToast(variant = null, text) {
            this.$bvToast.toast(text, {
                title: `${variant || "info"}`,
                variant: variant,
                solid: true,
            })
        },
        exportCSV() {
            try {
                if (!this.last_result || this.last_result.length < 1) {
                    this.makeToast("info", "There is nothing to export")
                    return
                }

                const replacer = (key, value) => (value === null ? "" : value) // specify how you want to handle null values here
                const header = Object.keys(this.last_result[0])

                const csv =
                    "data:text/csv;charset=utf-8," +
                    encodeURIComponent(
                        [
                            header
                                .map((el) => el.replaceAll("_", " "))
                                .join(","), // header row first
                            ...this.last_result.map((row) =>
                                header
                                    .map((fieldName) =>
                                        JSON.stringify(row[fieldName], replacer)
                                    )
                                    .join(",")
                            ),
                        ].join("\r\n")
                    )

                let fileName = "linkedin_data.csv"
                var aLink = document.createElement("a")
                aLink.download = fileName
                aLink.href = csv

                var event = new MouseEvent("click")
                aLink.dispatchEvent(event)
            } catch (err) {
                console.log(err)
                this.makeToast("danger", "Can't export")
            }
        },
        async loadAccounts() {
            try {
                let res = await axios.get(ACCOUNTS_API)
                let r = res.data
                if (r.code < 0) {
                    console.log(r)
                    this.makeToast(
                        "danger",
                        "Can't load accounts. Server error."
                    )
                } else {
                    this.account_data = r.data
                        .filter((el) => el.status === 0) // only active
                        .map((el) => {
                            return {
                                text: el.login != null ? el.login : el.li_at,
                                value: el._id,
                            }
                        })
                    console.log("accounts: ", this.account_data)
                }
            } catch (error) {
                let msg = "Error loading accounts. ERROR: " + error
                console.error(msg, error.stack)
                this.makeToast("danger", "Can't load accounts")
            }
        },
        async loadActions() {
            try {
                let res = await axios.post(ACCTION_API, {
                    input_data: { action: ACTION_TYPE },
                })
                let r = res.data
                if (r.code < 0) {
                    console.log(r)
                    this.makeToast(
                        "danger",
                        "Can't load actions. Server error."
                    )
                } else if (r.data) {
                    this.actions_data = r.data
                    if (this.actions_data.status === 0) {
                        this.makeToast("info", "Action in progress...")
                    } else if (this.actions_data.status === -1) {
                        // this.makeToast(
                        //     "danger",
                        //     "Something went wrong - empty result"
                        // )
                        console.log("Something went wrong - status '-1'")
                    }
                    try {
                        this.last_result = [JSON.parse(r.data.result_data.data)]
                    } catch (err) {
                        console.log(
                            "can't parse result data for actions: ",
                            r.data
                        )
                    }
                    console.log("Actions: ", this.actions_data)
                }

                this.formatResult()
            } catch (error) {
                let msg = "Error loading actions. ERROR: " + error
                console.error(msg, error.stack)
                this.makeToast("danger", "Can't load actions")
            }

            this.loaded = true
        },
        formatResult() {
            // replace arrays with strings
            if (!this.last_result || this.last_result.length < 1) return

            this.last_result = this.last_result.map((row) => {
                for (let key of Object.keys(row)) {
                    if (Array.isArray(row[key]) && row[key].length > 0)
                        row[key] = row[key].join(", ")
                    else if (Array.isArray(row[key]) && row[key].length === 0)
                        row[key] = ""
                }
                return row
            })

            console.log("last_result: ", this.last_result)
        },
        async refresh() {
            try {
                this.loaded = false
                await this.loadActions()
                this.makeToast("success", "Refreshed")
            } catch (err) {
                console.log(err)
            }
        },
        async search() {
            if (!this.selected_account) {
                this.makeToast("danger", "Select account")
                this.makeToast("danger", this.selected_account)
                return
            }

            if (this.linkedin == "") {
                this.makeToast("danger", "Empty profile link")
                return
            }

            if (
                !this.linkedin.includes("linkedin") ||
                !this.linkedin.includes("/in/")
            ) {
                this.makeToast(
                    "danger",
                    "Wrong link - past here link to Linkedin profile"
                )
                return
            }

            try {
                this.makeToast("info", "Action started")

                let res = await axios.post(SCRIBE_API, {
                    credentials_id: this.selected_account,
                    input_data: {
                        prospect_data: {
                            linkedin: this.linkedin,
                        },
                    },
                })

                let r = res.data
                if (r.code < 0) {
                    console.log(r)
                    this.makeToast(
                        "danger",
                        "Can't make this action. Server error."
                    )
                } else {
                    this.actions_data = r.data
                    try {
                        this.last_result = r.data.result_data.data.arr
                    } catch (err) {
                        console.log(
                            "can't parse result data for actions: ",
                            r.data
                        )
                    }
                    console.log("last_result: ", this.last_result)
                    this.makeToast(
                        "success",
                        "Completed. Check result on results tab."
                    )
                    await this.refresh()
                }
            } catch (error) {
                let msg = "Error loading actions. ERROR: " + error
                console.error(msg, error.stack)
                this.makeToast("danger", "Can't load actions")
            }
        },
    },
    async mounted() {
        await this.loadAccounts()
        await this.loadActions()
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
