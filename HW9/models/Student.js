const mongoose = require('mongoose');
const studentSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  study_hours: {
    type: Number,
    required: true,
    min: 0
  },
  attendance: {
    type: Number,
    required: true,
    min: 0
  },
  score: {
    type: Number,
    min: 0
  }
});

module.exports = mongoose.model('Student', studentSchema);