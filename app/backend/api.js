const express = require('express');
const { spawn } = require('child_process');

const app = express();
app.use(express.json());

app.post('/predict', (req, res) => {
  const inputData = req.body;

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

  // Send input JSON to python stdin
  python.stdin.write(JSON.stringify(inputData));
  python.stdin.end();
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`API server listening on port ${PORT}`);
});
