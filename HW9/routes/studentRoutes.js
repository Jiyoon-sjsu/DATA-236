const express = require('express');
const router = express.Router();

const {
    getStudents,
    addStudent,
    predictScore,
    updateStudent
} = require('../controllers/studentController');

// GET all students
router.get('/', getStudents);

// POST new student
router.post('/', addStudent);

// POST predict salary
router.post('/predict', predictScore);

// PUT update student
router.put('/:id', updateStudent);

module.exports = router;
