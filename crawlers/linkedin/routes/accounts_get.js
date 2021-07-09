const router = require("express").Router()
const models = require("../../models/models.js")

const MyExceptions = require("../../exceptions/exceptions.js")
var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")

/**
 * @swagger
 * /accounts:
 *   post:
 *     summary: Get all your Linkedin accounts.
 *     description: Get all your Linkedin accounts.
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
 *         description: Account
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
 *                 data:
 *                   type: object
 *                   properties:
 *                      _id:
 *                          type: integer
 *                          description: credentials_id for next requests
 *                          example: 1589
 */
router.post("/accounts", async (req, res) => {
    let result_data = {}
    let task = req.body

    try {
        let accounts = await models.Accounts.find({ user_id: task.user._id })

        console.log("... accounts: ... ", accounts)

        result_data = {
            code: 0,
            if_true: true,
            data: accounts,
        }
    } catch (err) {
        log.error("Get accounts error:", err.stack)

        status = status_codes.FAILED

        result_data = {
            if_true: false,
            code: -1,
            raw: err,
        }
    }

    log.debug("Get accounts RES: ", result_data)
    return res.json(result_data)
})

module.exports = router
