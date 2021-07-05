const express = require("express")
//const mongoose = require("mongoose")
const config = require("./config")
const routes = require("./linkedin/routes/workers")

const swaggerUi = require("swagger-ui-express")
const swaggerJSDoc = require('swagger-jsdoc');

const swaggerDefinition = {
  openapi: '3.0.0',
  info: {
    title: 'Linkedin API pasrer',
    version: '1.0.0',
  },
};

const options = {
  swaggerDefinition,
  // Paths to files containing OpenAPI definitions
  apis: ['./linkedin/routes/*.js'],
};

const swaggerSpec = swaggerJSDoc(options);

var log = require("loglevel").getLogger("o24_logger")

const app = express()

//app.use(express.urlencoded({ extended: true })) // use = add new middleware
app.use(express.json())
app.use(express.urlencoded())

// swagger
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec))

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
app.use(routes)

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
                `... Server started in ${APP_ENV == null ? "Test" : APP_ENV} mode ...`,
            )
        })
    } catch (e) {
        log.error("..... Server error: .....", e)
    }
}

start()
