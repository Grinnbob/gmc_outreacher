const express = require("express")
const fs = require("fs")
//const mongoose = require("mongoose")
const config = require("./config")
const models = require("./models/models.js")
const swaggerUi = require("swagger-ui-express")
const swaggerDocument = require('./swagger.json')
const authMiddleware = require('./middleware/auth')

const routes_path = "./linkedin/routes/"

var log = require("loglevel").getLogger("o24_logger")

const app = express()


app.use(express.json())
//app.use(express.urlencoded())
app.use(express.urlencoded({ extended: true }))

app.use(
    "/api-docs",
    swaggerUi.serve,
    swaggerUi.setup(swaggerDocument)
)

// check credentials
app.use(async (req, res, next) => {
    if (req.body.credentials_id) {
        let account = await models.Accounts.findOne({ _id: req.body.credentials_id })

        if (account == null) return next("Account not found")
        if (account.status === -1) return next("Account deleted")
        if (account.status === -2) return next("Account blocked")

        log.debug("account checked")
    }

    next()
})

// app.use(async (req, res, next) => {
//     console.log('migration started')

//     let actions = await models.Actions.find()
//     for(let action of actions) {
//         action.started_at = Date.parse(action.started_at)
//         action.finished_at = Date.parse(action.finished_at)
//         await models.Actions.findOneAndUpdate({ _id: action._id }, action)
//     }

//     console.log('migrated: ', actions.length)
// })

// Add headers
//app.use(function (req, res, next) {
    // res.setHeader("Access-Control-Allow-Origin", "*")
    // res.setHeader("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE")
    // res.setHeader(
    //     "Access-Control-Allow-Headers",
    //     "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    // )

    //res.setHeader('Access-Control-Allow-Credentials', true)

    // // Pass to next layer of middleware
    //next()
//})


var checkUserFilter = async function(req, res, next) {
    if(req._parsedUrl.pathname === '/user/create' || req._parsedUrl.pathname === '/auth') {
        next()
    } else {
        await authMiddleware(req, res, next)
    }
}

app.use(checkUserFilter)

fs.readdirSync(routes_path).forEach(function (file) {
    app.use(require(routes_path + file))
})

// const routes = require(routes_path)
// app.use('/', routes)

async function start() {
    try {
        // todo
        // start DB
        // await mongoose.connect(config.mongo.host + config.mongo.port, {
        //     useNewUrlParser: true,
        //     useFindAndModify: false,
        // })

        // logger
        let APP_ENV = process.env.APP_ENV

        // 0 = for tests, 4 = for Production
        if (APP_ENV == "Production") {
            log.setLevel("ERROR") // TRACE: 0, DEBUG: 1, INFO: 2, WARN: 3, ERROR: 4, SILENT: 5
        } else {
            log.setLevel("TRACE") // TRACE: 0, DEBUG: 1, INFO: 2, WARN: 3, ERROR: 4, SILENT: 5
        }

        // start server
        app.listen(config.server.port, config.server.host, (error) => {
            if (error) {
                log.error("... Unable to listen for connections", error)
                process.exit(10)
            }

            console.log(
                `... Server started at ${
                    config.server.host + ":" + config.server.port
                } ...`
            )

            log.error(
                `... Server started in ${
                    APP_ENV == null ? "Test" : APP_ENV
                } mode ...`
            )
        })
    } catch (e) {
        log.error("..... Server error: .....", e)
    }
}

start()
