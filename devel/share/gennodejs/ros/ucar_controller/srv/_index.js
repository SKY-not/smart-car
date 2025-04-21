
"use strict";

let SetLEDMode = require('./SetLEDMode.js')
let GetBatteryInfo = require('./GetBatteryInfo.js')
let SetMaxVel = require('./SetMaxVel.js')
let GetMaxVel = require('./GetMaxVel.js')
let GetSensorTF = require('./GetSensorTF.js')
let SetSensorTF = require('./SetSensorTF.js')

module.exports = {
  SetLEDMode: SetLEDMode,
  GetBatteryInfo: GetBatteryInfo,
  SetMaxVel: SetMaxVel,
  GetMaxVel: GetMaxVel,
  GetSensorTF: GetSensorTF,
  SetSensorTF: SetSensorTF,
};
