const router = require("express").Router()
const models = require("../../models/models.js")

const MyExceptions = require("../../exceptions/exceptions.js")
var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")

/*
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
router.post("/account", async (req, res) => {
    let result_data = {}
    let task = req.body

    if( !task.input_data ) return res.status(403).send("Wrong input data format - empty input_data.").end()
    let input_data = task.input_data
    if( !input_data.login ) return res.status(403).send("Wrong input data format - login required.").end()
    if( !input_data.password && !input_data.li_at ) return res.status(403).send("Wrong input data format - li_at or password required.").end()

    try {
        // create account
        let account = await models.Accounts.create({
            login: input_data.login,
            password: input_data.password,
            user_id: task.userId,
            cookies: input_data.li_at
                ? [
                      {
                          name: "li_at",
                          value: input_data.li_at,
                          domain: ".www.linkedin.com",
                          path: "/",
                          expires: Date.now() / 1000 + 10000000, // + ~ 4 months // https://www.epochconverter.com/
                          size: new TextEncoder().encode(input_data.li_at)
                              .length,
                          httpOnly: true,
                          secure: true,
                          session: false,
                          sameSite: "None",
                      },
                  ]
                : null,
            expires: input_data.li_at ? Date.now() / 1000 + 10000000 : 0,
        })

        console.log("...created account: ... ", account)

        result_data = {
            code: 0,
            if_true: true,
            data: {
                _id: account._id,
            },
        }
    } catch (err) {
        log.error("create account error:", err.stack)

        status = status_codes.FAILED

        result_data = {
            if_true: false,
            code: -1,
            raw: err,
        }
    }

    log.debug("Create account RES: ", result_data)
    return res.json(result_data)
})

module.exports = router
