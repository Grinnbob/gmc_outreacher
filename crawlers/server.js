const express = require("express")
const fs = require("fs")
//const mongoose = require("mongoose")
const config = require("./config")
//const routes = require("./linkedin/routes/*.js")
const models = require("./models/models.js")

const swaggerUi = require("swagger-ui-express")
const swaggerJSDoc = require("swagger-jsdoc")

const routes_path = "./linkedin/routes/"

const swaggerDefinition = {
    openapi: "3.0.0",
    info: {
        title: "Linkedin API pasrer",
        version: "1.0.0",
    },
}

const options = {
    swaggerDefinition,
    // Paths to files containing OpenAPI definitions
    apis: ["./linkedin/routes/*.js"],
}

const swaggerSpec = swaggerJSDoc(options)

var log = require("loglevel").getLogger("o24_logger")

const app = express()

// auth
const session = require("express-session")
const passport = require("passport")
const localStrategy = require("passport-local").Strategy
const flash = require("connect-flash")

passport.serializeUser((user, done) => done(null, user))
passport.deserializeUser((user, done) => done(null, user))

app.use(express.json())
//app.use(express.urlencoded())
app.use(express.urlencoded({ extended: true }))

app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec)) // swagger

/// auth
app.use(session({ secret: "Linkedin_API_secret_8" }))
app.use(flash())
app.use(passport.initialize())
app.use(passport.session())
app.use(async (req, res, next) => {
    if (req.body.login && req.body.password) {
        req.body.user = await models.Users.findOne({ login: req.body.login })

        if (req.body.user == null)
            return next("User not found")
        else if (req.body.password !== req.body.user.password)
            return next("Wrong password")

        log.debug("User checked")

        next()
    } else {
        log.error("Auth error - empty login / password in request")
    }
})

passport.use(
    new localStrategy(async (login, password, done) => {
        let user = await models.Users.findOne({ login: login })

        if (user == null)
            return done(null, false, {
                message: "User not found",
            })
        else if (password !== user.password)
            return done(null, false, {
                message: "Wrong password",
            })

        return done(null, user)
    })
)

// Add headers
app.use(function (req, res, next) {
    res.setHeader("Access-Control-Allow-Origin", "*")
    res.setHeader("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE")
    res.setHeader(
        "Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    )

    // Pass to next layer of middleware
    next()
})

//app.use('/bs/api', require('./api/router'))
//app.use(routes)
fs.readdirSync(routes_path).forEach(function (file) {
    console.log(routes_path + file)
    app.use(require(routes_path + file))
})

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
