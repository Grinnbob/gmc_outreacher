module.exports = {
    server: {
        host: process.env.HOST || "mongodb://127.0.0.1",
        port: process.env.PORT || 27017,
    },
    mongo: {
        host: process.env.HOST || "mongodb://127.0.0.1",
        port: process.env.PORT || 27017,
    },
}
