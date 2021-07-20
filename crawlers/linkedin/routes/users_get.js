const router = require("express").Router()
const Bcrypt = require('bcryptjs')

const models = require("../../models/models.js")
var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")
const BCRYPT_ROUNDS = 10


router.get("/users", async (req, res) => {
    let result_data = {}
    // todo check here admin role else 403

    try {
        let users = await models.Users.find()

        result_data = {
            if_true: true,
            code: 0,
            data: JSON.stringify(users)
        }
    } catch (err) {
        log.error("Get users error:", err.stack)

        status = status_codes.FAILED

        result_data = {
            if_true: false,
            code: -1,
            raw: err,
        }
    }

    log.debug("Create user RES: ", result_data)
    return res.json(result_data)
})

module.exports = router
