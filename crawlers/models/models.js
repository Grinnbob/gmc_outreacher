let mongooseConnect = require("./connect.js")
let mongoose = mongooseConnect.mongoose
let Schema = mongoose.Schema

let accountsSchema = new Schema({
    task_id: {
        type: mongoose.ObjectId,
        default: null,
    },

    user_id: {
        type: mongoose.ObjectId,
    },

    status: {
        type: Number,
        default: 0,
    },

    login: {
        type: String,
        default: null,
    },

    password: {
        type: String,
        default: null,
    },

    expires: Number,

    cookies: {
        type: Array,
        default: null,
    },

    blocking_type: {
        type: String,
        default: null,
    },

    blocking_data: {
        type: Object,
        default: null,
    },
})

let userSchema = new Schema({
    login: {
        type: String,
    },

    password: {
        type: String,
    },

    token: {
        type: String,
        default: null,
    },

    status: {
        type: Number,
        default: 0, // 0 = test user, 1 = active, 2 = archived
    },
})

let actionSchema = new Schema({
    action: {
        type: Number, // action type
    },

    user_id: {
        type: mongoose.ObjectId,
    },

    timestamp: {
        type: String,
        default: null,
    },

    status: {
        type: Number,
        default: 0, // exit status: 0 = in progress, 1 = done, -1 = exit with error
    },

    input_data: Object,

    result_data: Object,

    ack: {
        type: Number, // 1 = in work, 0 = free
        default: 0,
    },

    is_queued: {
        type: Number,
        default: 0,
    },

    blocking_data: Object,
})

let cronLockSchema = new Schema({
    lock: {
        type: String,
        unique: true, // it's needed to prevent creating new documents. always 1 document with lock = cron_lock
    },

    ack: {
        type: Number,
        default: 0,
    },
})

module.exports = {
    Accounts: mongoose.model("Accounts", accountsSchema),
    CronLock: mongoose.model("CronLock", cronLockSchema),
    Users: mongoose.model("Users", userSchema),
    Actions: mongoose.model("Actions", actionSchema),
}
