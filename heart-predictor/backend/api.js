const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');

const app = express();
app.use(cors()); // Allow frontend to call this API
app.use(express.json());

app.post('/predict', (req, res) => {
  const inputData = req.body;

  // Spawn the Python script
  const python = spawn('python3', ['predict.py']);

  let output = '';
  let error = '';

  python.stdout.on('data', (data) => {
    output += data.toString();
  });

  python.stderr.on('data', (data) => {
    error += data.toString();
  });

  python.on('close', (code) => {
    if (code !== 0) {
      res.status(500).json({ error: error || 'Unknown error' });
      return;
    }
    try {
      const prediction = JSON.parse(output);
      res.json(prediction);
    } catch (e) {
      res.status(500).json({ error: 'Failed to parse prediction output' });
    }
  });

  // Send JSON to Python's stdin
  python.stdin.write(JSON.stringify(inputData));
  python.stdin.end();
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`✅ API server running on port ${PORT}`);
});
