// Auto-generated. Do not edit!

// (in-package radiation_pub.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class radiation {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.radiation = null;
    }
    else {
      if (initObj.hasOwnProperty('radiation')) {
        this.radiation = initObj.radiation
      }
      else {
        this.radiation = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type radiation
    // Serialize message field [radiation]
    bufferOffset = _arraySerializer.float64(obj.radiation, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type radiation
    let len;
    let data = new radiation(null);
    // Deserialize message field [radiation]
    data.radiation = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.radiation.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'radiation_pub/radiation';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'ae3ed639d310a116f0319906c7d3e096';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] radiation
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new radiation(null);
    if (msg.radiation !== undefined) {
      resolved.radiation = msg.radiation;
    }
    else {
      resolved.radiation = []
    }

    return resolved;
    }
};

module.exports = radiation;
