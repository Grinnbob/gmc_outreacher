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
 * /search:
 *   post:
 *     summary: Scribe from Linkedin search.
 *     description: Scribe linkedin links, names, job, company of members from Linkedin search page.
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
 *                                  campaign_data:
 *                                      type: object
 *                                      properties:
 *                                          search_url:
 *                                              type: string
 *                                              description: search URL.
 *                                              example: www.linkedin.com/user/search=marketers
 *                                          interval_pages:
 *                                              type: integer
 *                                              description: interval between pages scribe.
 *                                              example: 10
 *     responses:
 *       200:
 *         description: A list of users.
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
 *                      link:
 *                          type: string
 *                          description: search link
 *                          example: www.linkedin.com/user/search=marketers
 *                      arr:
 *                          type: array
 *                          items:
 *                              type: object
 *                              properties:
 *                                  linkedin:
 *                                      type: string
 *                                      description: member link
 *                                      example: www.linkedin.com/some_user
 *                                  full_name:
 *                                      type: string
 *                                      description: The user's full name.
 *                                      example: Leanne Graham
 *                                  first_name:
 *                                      type: string
 *                                      description: The user's first name.
 *                                      example: Leanne
 *                                  last_name:
 *                                      type: string
 *                                      description: The user's last name.
 *                                      example: Graham
 *                                  job_title:
 *                                      type: string
 *                                      description: The user's job title.
 *                                      example: Product Marketing Manager
 *                                  company_name:
 *                                      type: string
 *                                      description: The user's company.
 *                                      example: Morningstar
 */
router.post("/search", async (req, res) => {
    let status = status_codes.FAILED
    let result_data = {}
    let task = req.body
    let credentials_id = null
    let action = null

    let browser = null

    if( !task.input_data ) return res.status(400).send("Wrong input data format - empty input_data.").end()
    if( !task.credentials_id ) return res.status(400).send("Wrong input data format - empty credentials_id.").end()

    try {
        credentials_id = task.credentials_id
        let input_data = task.input_data
        let task_data = utils.serialize_data(input_data)

        if( !task_data.campaign_data ) return res.status(400).send("Wrong input data format.").end()
        if( !task_data.campaign_data.search_url ) return res.status(400).send("Wrong input data format.").end()
        if( !task_data.campaign_data.interval_pages ) return res.status(400).send("Wrong input data format.").end()

        try {
            // create action
            action = await models.Actions.create({
                action: action_codes.linkedin_search,
                user_id: task.userId,
                started_at: Date.now(),
                status: 0,
                ack: 1,
                input_data: input_data,
                result_data: result_data,
            })
        } catch (err) {
            throw new Error(
                `Can't save action for ${action_codes.linkedin_search} for user ${task.userId}: ${err}`
            )
        }

        let cookies = await utils.get_cookies(credentials_id)

        // start work
        searchAction = new modules.searchAction.SearchAction(
            cookies,
            credentials_id,
            task_data.campaign_data.search_url,
            task_data.campaign_data.interval_pages
        )
        browser = await searchAction.startBrowser()
        result_data = await searchAction.search()
        browser = await searchAction.closeBrowser()

        status = result_data.code >= 0 ? 5 : -1 // if we got some exception (BAN?), we have to save results before catch Error and send task status -1
    } catch (err) {
        log.error("searchWorker error:", err.stack)

        status = status_codes.FAILED

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
                code: MyExceptions.SearchWorkerError().code,
                raw: MyExceptions.SearchWorkerError(
                    "searchWorker error: " + err
                ).error,
            }
        }
    } finally {
        log.debug("SearchWorker RES: ", result_data)

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
