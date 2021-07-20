const router = require("express").Router()
const models = require("../../models/models.js")

const MyExceptions = require("../../exceptions/exceptions.js")
var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")

/**
 * @swagger
 * /account/delete:
 *   post:
 *     summary: Delete Linkedin account.
 *     description: Delete Linkedin account.
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
 *                          input_data:
 *                              type: object
 *                              properties:
 *                                  login:
 *                                    type: string
 *                                    description: Linkedin login
 *                                    example: linkedinlogin@gmail.com
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
 *                   description: account deleted
 *                   example: false
 */
router.post("/account/delete", async (req, res) => {
    let result_data = {}
    let task = req.body

    if( !task.input_data ) return res.status(400).send("Wrong input data format - empty input_data.").end()
    let input_data = task.input_data
    if( !input_data.login ) return res.status(400).send("Wrong input data format - login required.").end()

    try {
        // deactivate account
        let account = await models.Accounts.findOneAndUpdate({
            //_id: task.credentials_id,
            login: input_data.login,
            user_id: task.userId,
        }, {
            status: -1
        })

        //let account = await models.Accounts.deleteOne({ _id: input_data.login})

        console.log("...deactivated account: ... ", account)

        result_data = {
            code: 0,
            if_true: true,
        }
    } catch (err) {
        log.error("deactivate account error:", err.stack)

        status = status_codes.FAILED

        result_data = {
            if_true: false,
            code: -1,
            raw: err,
        }
    }

    log.debug("Deactivate account RES: ", result_data)
    return res.json(result_data)
})

module.exports = router
