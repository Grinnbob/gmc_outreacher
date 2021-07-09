const router = require("express").Router()

const models = require("../../models/models.js")

const MyExceptions = require("../../exceptions/exceptions.js")
var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")

/**
 * @swagger
 * /user:
 *   post:
 *     summary: Create user.
 *     description: Create user.
 *     requestBody:
 *          required: true
 *          content:
 *              application/json:
 *                  schema:
 *                      type: object
 *                      properties:
 *                          login:
 *                              type: string
 *                              description: service login
 *                              example: servicelogin@gsuit.com
 *                          password:
 *                              type: string
 *                              description: service password
 *                              example: mypass1234
 *     responses:
 *       200:
 *         description: user
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 code:
 *                   type: integer
 *                   description: status code
 *                   example: 0
 *                 if_true:
 *                   type: boolean
 *                   description: some expression
 *                   example: false
 */
router.post("/user", async (req, res) => {
    let result_data = {}
    let task = req.body
    console.log("...task: ...", task)

    try {
        // create user
        let user = await models.Users.create({
            login: task.login,
            password: task.password,
        })

        console.log("... user created: ...", user)

        result_data = {
            if_true: true,
            code: 0,
            data: {
                login: user.login,
            },
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
