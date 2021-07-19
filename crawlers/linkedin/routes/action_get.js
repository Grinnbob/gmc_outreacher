const router = require("express").Router()
const models = require("../../models/models.js")

var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")

/**
 * @swagger
 * /action:
 *   post:
 *     summary: Get last action.
 *     description: Get last action.
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
 *                   description: result data of last action
 *                   example: {}
 */
router.post("/action", async (req, res) => {
    let result_data = {}
    let task = req.body
    let action = {}

    try {
        let actions = []
        if (task.input_data && task.input_data.action) actions = await models.Actions.find({ user_id: task.userId, action: task.input_data.action }).sort('-started_at')
        else actions = await models.Actions.find({ user_id: task.userId }).sort('-started_at')

        action = actions[actions.length - 1]

        console.log("... action: ... ", action)

        result_data = {
            code: 0,
            if_true: true,
            data: action,
        }
    } catch (err) {
        log.error("Get action error:", err.stack)

        status = status_codes.FAILED

        result_data = {
            if_true: false,
            code: -1,
            raw: err,
        }
    }

    log.debug("Get action RES: ", result_data)
    return res.json(result_data)
})

module.exports = router
