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
 * /message:
 *   post:
 *     summary: Message Linkedin member.
 *     description: Message Linkedin member by link.
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
 *                                          first_name:
 *                                              type: string
 *                                              description: member first name.
 *                                              example: "Nikola"
 *                                  template_data:
 *                                      type: object
 *                                      properties:
 *                                          message:
 *                                              type: string
 *                                              description: message to member
 *                                              example: "Hi, {first_name}! How are you today?"
 *     responses:
 *       200:
 *         description: Connected or not
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
 *                   description: true if request has been sent
 *                   example: false
 */
router.post("/message", async (req, res) => {
    let status = status_codes.FAILED
    let result_data = {}
    let task = req.body
    let credentials_id = null

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

        let cookies = await utils.get_cookies(credentials_id)

        // start work
        // check reply
        let messageCheckAction =
            new modules.messageCheckAction.MessageCheckAction(
                cookies,
                credentials_id,
                task_data.prospect_data.linkedin
            )
        browser = await messageCheckAction.startBrowser()
        let resCheckMsg = await messageCheckAction.messageCheck()
        browser = await messageCheckAction.closeBrowser()

        if (!resCheckMsg.if_true) {
            // if no reply - send msg
            let messageAction = new modules.messageAction.MessageAction(
                cookies,
                credentials_id,
                task_data.prospect_data.linkedin,
                task_data.prospect_data,
                task_data.template_data.message
            )
            browser = await messageAction.startBrowser()
            let res = await messageAction.message()
            browser = await messageAction.closeBrowser()

            result_data = {
                code: 0,
                if_true: res,
            }
        } else {
            // else - task finished
            result_data = resCheckMsg
        }
        status = status_codes.CARRYOUT
    } catch (err) {
        log.error("messageWorker error:", err.stack)

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
                code: MyExceptions.MessageWorkerError().code,
                raw: MyExceptions.MessageWorkerError(
                    "messageWorker error: " + err
                ).error,
            }
        }
        status = status_codes.FAILED
    } finally {
        log.debug("MessageWorker RES: ", result_data)

        if (browser != null) {
            await browser.close()
            browser.disconnect()
        }
    }

    return res.json(result_data)
})

module.exports = router
