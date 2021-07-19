const asyncHandler = require('express-async-handler')
const models = require("../models/models.js")


const authMiddleware = asyncHandler(async (req, res, next) => {
  const tokenAuthResult = await tokenAuth(req);
  if (tokenAuthResult.success) return next();

  res.status(tokenAuthResult.code);
  if (tokenAuthResult.message) {
    res.send(tokenAuthResult.message)
  } else {
    res.end()
  }
});

const tokenAuth = async (req) => {
  const token = req.get('authorization');
  console.log(token);
  if (!token) return { success: false, code: 401 };

  const verifyResult = await verifyToken({ token });

  if (!verifyResult.success) return { success: false, code: verifyResult.code, message: verifyResult.message };
  req.body.userId = verifyResult.userId;
  return { success: true };
};

const verifyToken = async ({ token }) => {
    const userFromDB = await models.Users.findOne({ token: token });
  
    if (!userFromDB) return { success: false, message: 'Token not found', code: 401 };
    const now = Date.now();
    if (userFromDB.tokenExpiresAt < now) return { success: false, message: 'Token not found', code: 401 };
  
    return { success: true, userId: userFromDB._id };
};

module.exports = authMiddleware;