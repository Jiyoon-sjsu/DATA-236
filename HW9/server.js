const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
// const employeeRoutes = require('./routes/employeeRoutes');
const studentRoutes = require('./routes/studentRoutes');

const app = express();
app.use(cors()); 
app.use(express.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/HW9', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log(" MongoDB connected"))
.catch(err => console.error(" MongoDB connection error:", err));

// Use employee routes
// app.use('/api/employees', employeeRoutes);

// Use student routes
app.use('/api/students', studentRoutes);

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(` Server running on port ${PORT}`));
