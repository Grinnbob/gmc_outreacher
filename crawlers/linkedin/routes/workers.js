const router = require("express").Router()
const jwt = require("jsonwebtoken")

const modules = require("../modules.js")
//const models_shared = require("../../models/shared.js")
const models = require("../../models/models.js")

const MyExceptions = require("../../exceptions/exceptions.js")
var log = require("loglevel").getLogger("o24_logger")

const status_codes = require("../status_codes")
const action_codes = require("../action_codes").action_codes

// todo https://habr.com/ru/company/ruvds/blog/457700/
function generateToken(user) {
    const data = {
        _id: user._id,
        name: user.name,
        login: user.login,
    }
    const signature = "abcdSUPERLINKEDINAPPqwerty000"
    const expiration = "7d"

    return jwt.sign({ data }, signature, { expiresIn: expiration })
}

async function get_cookies(credentials_id) {
    let account = await models.Accounts.findOne(
        { _id: credentials_id },
        function (err, res) {
            if (err)
                throw MyExceptions.MongoDBError(
                    "MongoDB find account err: " + err
                )
        }
    )

    if (account == null) {
        throw new Error(
            "get_cookies: Account not found with credentials_id:",
            credentials_id
        )
    }

    const is_expired = check_expired(account) // true if we have to update cookies

    if (
        account.cookies == null ||
        !Array.isArray(account.cookies) ||
        account.cookies.length <= 0 ||
        is_expired
    ) {
        let loginAction = new modules.loginAction.LoginAction(credentials_id)
        await loginAction.startBrowser()
        await loginAction.login()
        await loginAction.closeBrowser()

        account = await models.Accounts.findOne(
            { _id: credentials_id },
            function (err, res) {
                if (err)
                    throw MyExceptions.MongoDBError(
                        "MongoDB find account err: " + err
                    )
            }
        )

        return account.cookies
    }

    return account.cookies
}

function check_expired(account) {
    if (account.expires == null) {
        log.debug(
            "check_expired: expires is null, credentials_id:",
            account._id
        )
        return true
    }

    if (Date.now() / 1000 > account.expires) {
        log.debug("check_expired: expires is OLD, credentials_id:", account._id)
        log.debug("check_expired: account.expires:", account.expires)
        log.debug("check_expired: expires now:", Date.now() / 1000)
    }

    return Date.now() / 1000 > account.expires
}

function serialize_data(input_data) {
    if (input_data == null) {
        throw new Error("SERIALIZATION error: input_data can’t be empty")
    }

    let task_data = {}

    task_data["campaign_data"] = input_data.campaign_data
    task_data["template_data"] = input_data.template_data
    task_data["prospect_data"] = input_data.prospect_data

    return task_data
}

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
        let user = await models.Users.create(
            { login: task.login, password: task.password },
            function (err_db, res) {
                if (err_db)
                    throw MyExceptions.MongoDBError(
                        "MongoDB create user err: " + err_db
                    )
            }
        )

        console.log("... user created: ...", user)

        result_data = {
            if_true: false,
            code: 0,
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

/**
 * @swagger
 * /account:
 *   post:
 *     summary: Add Linkedin account.
 *     description: Add Linkedin account.
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
 *                                  password:
 *                                    type: string
 *                                    description: Linkedin password
 *                                    example: mypass1234
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
    console.log("...task...", task)

    try {
        let input_data = task.input_data
        if (!input_data) {
            throw new Error("there is no task.input_data")
        }
        console.log("input_data: ", input_data)

        // create account
        await models.Accounts.create(
            {
                login: input_data.login,
                password: input_data.password,
                user_id: task.user._id,
            },
            function (err_db, res) {
                if (err_db)
                    throw MyExceptions.MongoDBError(
                        "MongoDB create account err: " + err_db
                    )
            }
        )

        let account = await models.Accounts.findOne(
            { login: input_data.login },
            function (err_db, res) {
                if (err_db)
                    throw MyExceptions.MongoDBError(
                        "MongoDB find account err: " + err_db
                    )
            }
        )

        console.log("...created account: ... ", account)

        result_data._id = account._id
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
 *                              type: integer
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
    console.log("...task...", task)

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
        let task_data = serialize_data(input_data)

        try {
            // create action
            action = await models.Actions.create({
                action: action_codes.linkedin_search,
                user_id: task.user._id,
                timestamp: new Date(),
                status: 0,
                ack: 1,
                input_data: input_data,
                result_data: result_data,
            })
        } catch (err) {
            throw new Error(
                `Can't save action for ${action_codes.linkedin_search} for user ${task.user._id}: ${err}`
            )
        }

        let cookies = await get_cookies(credentials_id)

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
                timestamp: new Date(),
                status: 1,
                ack: 0,
                result_data: result_data,
            }
        )
    } catch (err) {
        log.error(`Can't update action for ${req.login}`)
    }

    return res.json(result_data)
})

/**
 * @swagger
 * /sn/search:
 *   post:
 *     summary: Scribe from Linkedin Sales Navigator search.
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
 *                              type: integer
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
router.post("/sn/search", async (req, res) => {
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
        let task_data = serialize_data(input_data)

        try {
            // create action
            action = await models.Actions.create({
                action: action_codes.linkedin_search_sn,
                user_id: task.user._id,
                timestamp: new Date(),
                status: 0,
                ack: 1,
                input_data: input_data,
                result_data: result_data,
            })
        } catch (err) {
            throw new Error(
                `Can't save action for ${action_codes.linkedin_search_sn} for user ${task.user._id}: ${err}`
            )
        }

        let cookies = await get_cookies(credentials_id)

        // start work
        sn_searchAction = new modules.sn_searchAction.SN_SearchAction(
            cookies,
            credentials_id,
            task_data.campaign_data.search_url,
            task_data.campaign_data.interval_pages
        )
        browser = await sn_searchAction.startBrowser()
        result_data = await sn_searchAction.search()
        browser = await sn_searchAction.closeBrowser()

        status = result_data.code >= 0 ? 5 : -1 // if we got some exception (BAN?), we have to save results before catch Error and send task status -1
    } catch (err) {
        log.error("sn_searchWorker error:", err.stack)

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
                code: MyExceptions.SN_SearchWorkerError().code,
                raw: MyExceptions.SN_SearchWorkerError(
                    "sn_searchWorker error: " + err
                ).error,
            }
        }
    } finally {
        log.debug("sn_searchWorker RES: ", result_data)

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
                timestamp: new Date(),
                status: 1,
                ack: 0,
                result_data: result_data,
            }
        )
    } catch (err) {
        log.error(`Can't update action for ${req.login}`)
    }

    return res.json(result_data)
})

router.post("/connect", async (req, res) => {
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
        let task_data = serialize_data(input_data)

        let cookies = await get_cookies(credentials_id)

        // start work
        let message = ""
        if (task_data.template_data != null) {
            if (task_data.template_data.message != null)
                message = task_data.template_data.message
        }

        let connectAction = new modules.connectAction.ConnectAction(
            cookies,
            credentials_id,
            task_data.prospect_data.linkedin,
            message,
            task_data.prospect_data
        )
        browser = await connectAction.startBrowser()
        res = await connectAction.connect()
        browser = await connectAction.closeBrowser()

        result_data = {
            code: 0,
            if_true: res,
        }
        status = status_codes.CARRYOUT
    } catch (err) {
        log.error("connectWorker error:", err.stack)

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
                code: MyExceptions.ConnectWorkerError().code,
                raw: MyExceptions.ConnectWorkerError(
                    "connectWorker error: " + err
                ).error,
            }
        }
        status = status_codes.FAILED
    } finally {
        log.debug("ConnectWorker RES: ", result_data)

        if (browser != null) {
            await browser.close()
            browser.disconnect()
        }
    }

    return res.json(result_data)
})

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
        let task_data = serialize_data(input_data)

        let cookies = await get_cookies(credentials_id)

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

router.post("/scribe", async (req, res) => {
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
        let task_data = serialize_data(input_data)

        let cookies = await get_cookies(credentials_id)

        // start work
        let scribeAction = new modules.scribeAction.ScribeAction(
            cookies,
            credentials_id,
            task_data.prospect_data.linkedin
        )
        browser = await scribeAction.startBrowser()
        let res = await scribeAction.scribe()
        browser = await scribeAction.closeBrowser()

        result_data = {
            code: 0,
            if_true: true,
            data: JSON.stringify(res),
        }
        status = status_codes.CARRYOUT
    } catch (err) {
        log.error("scribeWorker error:", err.stack)

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
                code: MyExceptions.ScribeWorkerError().code,
                raw: MyExceptions.ScribeWorkerError(
                    "scribeWorker error: " + err
                ).error,
            }
        }
        status = status_codes.FAILED
    } finally {
        log.debug("ScribeWorker RES: ", result_data)

        if (browser != null) {
            await browser.close()
            browser.disconnect()
        }
    }

    return res.json(result_data)
})

router.post("/sn/scribe", async (req, res) => {
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
        let task_data = serialize_data(input_data)

        let cookies = await get_cookies(credentials_id)

        // start work
        let sn_scribeAction = new modules.sn_scribeAction.SN_ScribeAction(
            cookies,
            credentials_id,
            task_data.prospect_data.linkedin_sn
        )
        browser = await sn_scribeAction.startBrowser()
        let res = await sn_scribeAction.scribe()
        browser = await sn_scribeAction.closeBrowser()

        result_data = {
            code: 0,
            if_true: true,
            data: JSON.stringify(res),
        }
        status = status_codes.CARRYOUT
    } catch (err) {
        log.error("sn_scribeWorker error:", err.stack)

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
                code: MyExceptions.SN_ScribeWorkerError().code,
                raw: MyExceptions.SN_ScribeWorkerError(
                    "sn_scribeWorker error: " + err
                ).error,
            }
        }
        status = status_codes.FAILED
    } finally {
        log.debug("sn_scribeWorker RES: ", result_data)

        if (browser != null) {
            await browser.close()
            browser.disconnect()
        }
    }

    return res.json(result_data)
})

router.post("/message/check", async (req, res) => {
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
        let task_data = serialize_data(input_data)

        let cookies = await get_cookies(credentials_id)

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

    return res.json(result_data)
})

router.post("/connect/check", async (req, res) => {
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
        let task_data = serialize_data(input_data)

        let cookies = await get_cookies(credentials_id)

        // start work
        let connectCheckAction =
            new modules.connectCheckAction.ConnectCheckAction(
                cookies,
                credentials_id,
                task_data.prospect_data.linkedin
            )
        browser = await connectCheckAction.startBrowser()
        let res = await connectCheckAction.connectCheck()
        browser = await connectCheckAction.closeBrowser()

        result_data = {
            code: 0,
            if_true: res,
        }
        status = status_codes.CARRYOUT
    } catch (err) {
        log.error("connectCheckWorker error:", err.stack)

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
                code: MyExceptions.ConnectCheckWorkerError().code,
                raw: MyExceptions.ConnectCheckWorkerError(
                    "connectCheckWorker error: " + err
                ).error,
            }
        }
        status = status_codes.FAILED
    } finally {
        log.debug("ConnectCheckWorker RES: ", result_data)

        if (browser != null) {
            await browser.close()
            browser.disconnect()
        }
    }

    return res.json(result_data)
})

router.post("/profile/visit", async (req, res) => {
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
        let task_data = serialize_data(input_data)

        let cookies = await get_cookies(credentials_id)

        // start work
        let visitProfileAction =
            new modules.visitProfileAction.VisitProfileAction(
                cookies,
                credentials_id,
                task_data.prospect_data.linkedin
            )
        browser = await visitProfileAction.startBrowser()
        let res = await visitProfileAction.visit()
        browser = await visitProfileAction.closeBrowser()

        result_data = {
            code: 0,
            if_true: res,
        }
        status = status_codes.CARRYOUT
    } catch (err) {
        log.error("visitProfileWorker error:", err.stack)

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
                code: MyExceptions.VisitProfileWorkerError().code,
                raw: MyExceptions.VisitProfileWorkerError(
                    "visitProfileWorker error: " + err
                ).error,
            }
        }
        status = status_codes.FAILED
    } finally {
        log.debug("visitProfileWorker RES: ", result_data)

        if (browser != null) {
            await browser.close()
            browser.disconnect()
        }
    }

    return res.json(result_data)
})

router.post("/post/engagement", async (req, res) => {
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
        let task_data = serialize_data(input_data)

        let cookies = await get_cookies(credentials_id)

        // start work
        post_engagement_action =
            new modules.post_engagement_action.Post_engagement_action(
                cookies,
                credentials_id,
                task_data.campaign_data.post_url
            )
        browser = await post_engagement_action.startBrowser()
        result_data = await post_engagement_action.engagement()
        browser = await post_engagement_action.closeBrowser()

        status = status_codes.CARRYOUT
    } catch (err) {
        log.error("post_engagement_worker error:", err.stack)

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
                code: MyExceptions.PostEngagementWorkerError().code,
                raw: MyExceptions.PostEngagementWorkerError(
                    "post_engagement_worker error: " + err
                ).error,
            }
        }
    } finally {
        log.debug("post_engagement_worker RES: ", result_data)

        if (browser != null) {
            await browser.close()
            browser.disconnect()
        }
    }

    return res.json(result_data)
})

module.exports = router
