import express from 'express';
import multer from 'multer';
import fetch from 'node-fetch';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import FormData from 'form-data';  // Needed for forwarding uploads

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.static(path.join(__dirname, 'public')));

app.post('/upload', upload.single('image'), async (req, res) => {
  const flaskURL = 'http://127.0.0.1:5000/upload';
  const fileStream = fs.createReadStream(req.file.path);

  const form = new FormData();
  form.append('image', fileStream, req.file.originalname);

  const response = await fetch(flaskURL, {
    method: 'POST',
    body: form,
    headers: form.getHeaders()
  });

  const data = await response.json();
  res.json(data);
});

app.post('/upload2', upload.single('image'), async (req, res) => {
  const flaskURL = 'http://127.0.0.1:5000/upload2';
  const fileStream = fs.createReadStream(req.file.path);

  const form = new FormData();
  form.append('image', fileStream, req.file.originalname);

  const response = await fetch(flaskURL, {
    method: 'POST',
    body: form,
    headers: form.getHeaders()
  });

  const data = await response.json();
  res.json(data);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
