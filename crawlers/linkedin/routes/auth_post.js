const router = require("express").Router()
const Bcrypt = require('bcryptjs');
const Crypto = require('crypto');

const models = require("../../models/models.js")
var log = require("loglevel").getLogger("o24_logger")

const DAYS_EXPIRES = 7

/**
 * @swagger
 * /auth:
 *   post:
 *     summary: Auth.
 *     description: Get auth token.
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
 *               type: string
 *               description: access token
 *               example: edwe2134t5hybxdfre5tr4wed
 */
router.post("/auth", async (req, res) => {
    let accessToken
    let task = req.body

    if (!task.login) return res.status(400).send('Login must be defined')
    if (!task.password) return res.status(400).send('Password must be defined')

    try {
        let user = await models.Users.findOne({ login: task.login })
        if (!user) return res.status(401).send('User not found')

        if (!Bcrypt.compareSync(task.password, user.password)) return res.status(401).send('Invalid password')

        accessToken = Crypto.createHmac('md5', Crypto.randomBytes(512).toString()).update([].slice.call(arguments).join(':')).digest('hex');
    
        await models.Users.findOneAndUpdate({ _id: user._id }, {
            token: accessToken,
            tokenExpiresAt: (Date.now() + (DAYS_EXPIRES * 24 * 60 * 60 * 1000)) // DAYS_EXPIRES mode
        })

        let result_data = {
            code: 0,
            data: {
                token: accessToken,
                _id: user._id,
                login: user.login
            }
        }

        log.debug("result: ", result_data)
        
        return res.json(result_data)
        
    } catch (err) {
        log.error("auth user error:", err.stack)
    }
})

module.exports = router
