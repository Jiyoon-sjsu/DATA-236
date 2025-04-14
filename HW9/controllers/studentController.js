const Student = require('../models/Student');
const redis = require('redis');
const axios = require('axios');

// Create Redis client and connect
const redisClient = redis.createClient();
redisClient.connect().catch(console.error);

// GET all students (with Redis caching)
const getStudents = async (req, res) => {
  const cacheKey = 'all_students';

  try {
    const cachedStudents = await redisClient.get(cacheKey);
    if (cachedStudents) {
      console.log('Data from Redis Cache');
      return res.status(200).json(JSON.parse(cachedStudents));
    }

    const students = await Student.find();
    if (students.length > 0) {
      await redisClient.set(cacheKey, JSON.stringify(students), { EX: 30 });
      console.log('Data from MongoDB');
    }
    res.status(200).json(students);
  } catch (err) {
    console.error('Error fetching students:', err);
    res.status(500).json({ error: 'Server error' });
  }
};

// POST new student
const addStudent = async (req, res) => {
  try {
    const { name, study_hours, attendance, score } = req.body;

    const newStudent = new Student({
      name,
      study_hours,
      attendance,
      score
    });

    await newStudent.save();

    // Clear Redis cache for students after adding new data
    await redisClient.del('all_students');
    
    res.status(201).json(newStudent);
  } catch (err) {
    console.error('Error creating student:', err);
    res.status(500).json({ message: 'Error creating student' });
  }
};

// POST /api/students/predict - Predict score using FastAPI
const predictScore = async (req, res) => {
  try {
    const { study_hours, attendance } = req.body;

    if (study_hours == null || attendance == null) {
      return res.status(400).json({ error: 'Please provide both study_hours and attendance' });
    }

    // Make a request to FastAPI for score prediction
    const response = await axios.post('http://127.0.0.1:8000/predict', {
      study_hours,
      attendance
    });

    const predicted_score = response.data.predicted_score;

    res.status(200).json({
      study_hours,
      attendance,
      predicted_score
    });

  } catch (err) {
    console.error('Error predicting score:', err.message);
    if (err.response) {
      // FastAPI returned an error response
      return res.status(err.response.status).json({ error: err.response.data.error });
    }
    // Network or other errors
    res.status(500).json({ error: 'Error predicting score' });
  }
};

// PUT update student
const updateStudent = async (req, res) => {
  try {
    const { id } = req.params;
    const { name, study_hours, attendance, score } = req.body;

    // Find the student by ID and update the record
    const updatedStudent = await Student.findByIdAndUpdate(
      id,
      { name, study_hours, attendance, score },
      { new: true, runValidators: true } // Return the updated document and validate inputs
    );

    if (!updatedStudent) {
      return res.status(404).json({ error: 'Student not found' });
    }

    // Clear the cache for all students to ensure consistency
    await redisClient.del('all_students');

    res.status(200).json(updatedStudent);
  } catch (err) {
    console.error('Error updating student:', err);
    res.status(500).json({ error: 'Error updating student' });
  }
};

module.exports = {
  getStudents,
  addStudent,
  predictScore,
  updateStudent
};
