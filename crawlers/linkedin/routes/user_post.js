const router = require("express").Router()
const Bcrypt = require('bcryptjs')

const models = require("../../models/models.js")
var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")
const BCRYPT_ROUNDS = 10


router.post("/user/create", async (req, res) => {
    let result_data = {}
    let task = req.body

    if( !task.login ) return res.status(400).send("Wrong input data format.").end()
    if( !task.password ) return res.status(400).send("Wrong input data format.").end()

    try {
        let user = await models.Users.findOne({ login: task.login })

        if (user) {
            log.debug("User already exists")
            result_data = {
                if_true: false,
                code: -1,
                raw: 'User already exists',
            }

        } else {
            // create user
            user = await models.Users.create({
                login: task.login,
                password: Bcrypt.hashSync(task.password, BCRYPT_ROUNDS)
            })

            console.log("... user created: ...", user)

            result_data = {
                if_true: true,
                code: 0,
                data: user,
            }
        }
    } catch (err) {
        log.error("create user error:", err.stack)

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
