const models = require("../models/models.js")
const modules = require("./modules.js")
var log = require("loglevel").getLogger("o24_logger")
const MyExceptions = require("../exceptions/exceptions.js")

const jwt = require("jsonwebtoken")

// todo https://habr.com/ru/company/ruvds/blog/457700/
function generateToken(user) {
    const data = {
        _id: user._id,
        name: user.name,
        login: user.login,
    }
    const signature = "abcdSUPERLINKEDINAPPqwerty000"
    const expiration = "7d"

    return jwt.sign({ data }, signature, { expiresIn: expiration })
}

async function get_cookies(credentials_id) {
    let account = await models.Accounts.findOne(
        { _id: credentials_id },
        function (err, res) {
            if (err)
                throw MyExceptions.MongoDBError(
                    "MongoDB find account err: " + err
                )
        }
    )

    if (account == null) {
        throw new Error(
            "get_cookies: Account not found with credentials_id:",
            credentials_id
        )
    }

    const is_expired = check_expired(account) // true if we have to update cookies

    if (
        account.cookies == null ||
        !Array.isArray(account.cookies) ||
        account.cookies.length <= 0 ||
        is_expired
    ) {
        let loginAction = new modules.loginAction.LoginAction(credentials_id)
        await loginAction.startBrowser()
        await loginAction.login()
        await loginAction.closeBrowser()

        account = await models.Accounts.findOne(
            { _id: credentials_id },
            function (err, res) {
                if (err)
                    throw MyExceptions.MongoDBError(
                        "MongoDB find account err: " + err
                    )
            }
        )

        return account.cookies
    }

    return account.cookies
}

function check_expired(account) {
    if (account.expires == null) {
        log.debug(
            "check_expired: expires is null, credentials_id:",
            account._id
        )
        return true
    }

    if (Date.now() / 1000 > account.expires) {
        log.debug("check_expired: expires is OLD, credentials_id:", account._id)
        log.debug("check_expired: account.expires:", account.expires)
        log.debug("check_expired: expires now:", Date.now() / 1000)
    }

    return Date.now() / 1000 > account.expires
}

function serialize_data(input_data) {
    if (input_data == null) {
        throw new Error("SERIALIZATION error: input_data can’t be empty")
    }

    let task_data = {}

    task_data["campaign_data"] = input_data.campaign_data
    task_data["template_data"] = input_data.template_data
    task_data["prospect_data"] = input_data.prospect_data

    return task_data
}

module.exports = {
    get_cookies,
    serialize_data,
}
