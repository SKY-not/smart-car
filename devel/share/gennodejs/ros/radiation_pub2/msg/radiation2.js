// Auto-generated. Do not edit!

// (in-package radiation_pub2.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class radiation2 {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.radiation2 = null;
    }
    else {
      if (initObj.hasOwnProperty('radiation2')) {
        this.radiation2 = initObj.radiation2
      }
      else {
        this.radiation2 = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type radiation2
    // Serialize message field [radiation2]
    bufferOffset = _arraySerializer.float64(obj.radiation2, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type radiation2
    let len;
    let data = new radiation2(null);
    // Deserialize message field [radiation2]
    data.radiation2 = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.radiation2.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'radiation_pub2/radiation2';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9a7d2ef45bfc6a980a446dc09330c970';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] radiation2
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new radiation2(null);
    if (msg.radiation2 !== undefined) {
      resolved.radiation2 = msg.radiation2;
    }
    else {
      resolved.radiation2 = []
    }

    return resolved;
    }
};

module.exports = radiation2;
