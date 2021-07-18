const router = require("express").Router()
const utils = require("../utils")

const modules = require("../modules.js")
const models = require("../../models/models.js")

const MyExceptions = require("../../exceptions/exceptions.js")
var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")
const action_codes = require("../action_codes").action_codes

/**
 * @swagger
 * /message/check:
 *   post:
 *     summary: Check if Linkedin member sent reply.
 *     description: Check if Linkedin member sent reply.
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
 *                          credentials_id:
 *                              type: string
 *                              description: Credentials ID for login in Linkedin.
 *                              example: 5
 *                          input_data:
 *                              type: object
 *                              properties:
 *                                  prospect_data:
 *                                      type: object
 *                                      properties:
 *                                          linkedin:
 *                                              type: string
 *                                              description: member URL.
 *                                              example: www.linkedin.com/user/
 *     responses:
 *       200:
 *         description: Reply exists or not
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
 *                   description: true if reply has been sent
 *                   example: false
 */
router.post("/message/check", async (req, res) => {
    let status = status_codes.FAILED
    let result_data = {}
    let task = req.body
    let credentials_id = null
    let action = null

    let browser = null
    try {
        credentials_id = task.credentials_id
        if (!credentials_id) {
            throw new Error("there is no task.credentials_id")
        }
        let input_data = task.input_data
        if (!input_data) {
            throw new Error("there is no task.input_data")
        }
        let task_data = utils.serialize_data(input_data)

        try {
            // create action
            action = await models.Actions.create({
                action: action_codes.linkedin_check_reply,
                user_id: task.user._id,
                started_at: Date.now(),
                status: 0,
                ack: 1,
                input_data: input_data,
                result_data: result_data,
            })
        } catch (err) {
            throw new Error(
                `Can't save action for ${action_codes.linkedin_check_reply} for user ${task.user._id}: ${err}`
            )
        }

        let cookies = await utils.get_cookies(credentials_id)

        // start work
        let messageCheckAction =
            new modules.messageCheckAction.MessageCheckAction(
                cookies,
                credentials_id,
                task_data.prospect_data.linkedin
            )
        browser = await messageCheckAction.startBrowser()
        result_data = await messageCheckAction.messageCheck()
        browser = await messageCheckAction.closeBrowser()

        status = status_codes.CARRYOUT
    } catch (err) {
        log.error("messageCheckWorker error:", err.stack)

        if (err.code != null && err.code != -1) {
            result_data = {
                if_true: false,
                code: err.code,
                raw: err.error,
            }
        } else if (err.code == -1) {
            status = status_codes.BLOCK_HAPPENED
            // Context error
            result_data = {
                if_true: false,
                code: err.code,
                raw: err.error,
            }
        } else {
            result_data = {
                if_true: false,
                code: MyExceptions.MessageCheckWorkerError().code,
                raw: MyExceptions.MessageCheckWorkerError(
                    "messageCheckWorker error: " + err
                ).error,
            }
        }
        status = status_codes.FAILED
    } finally {
        log.debug("MessageCheckWorker RES: ", result_data)

        if (browser != null) {
            await browser.close()
            browser.disconnect()
        }
    }

    try {
        // update action
        await models.Actions.findOneAndUpdate(
            { _id: action._id },
            {
                finished_at: Date.now(),
                status: result_data.code >= 0 ? 1 : -1,
                ack: 0,
                result_data: result_data,
            }
        )
    } catch (err) {
        log.error(`Can't update action for ${task.user.login}`)
    }

    return res.json(result_data)
})

module.exports = router
