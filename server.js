const express = require('express');
const session = require('express-session');
const rateLimit = require('express-rate-limit');
const { exec } = require('child_process');
const crypto = require('crypto');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// ── SESSION ────────────────────────────────────────────
app.use(session({
  secret: crypto.randomBytes(64).toString('hex'), // strong random secret
  resave: false,
  saveUninitialized: true,
  cookie: { httpOnly: true }
}));

// ── RATE LIMITERS ──────────────────────────────────────
const generateLimiter = rateLimit({
  windowMs: 60 * 1000,      // 1 minute window
  max: 10,                   // max 10 CAPTCHA generations per minute
  message: { error: 'Too many requests. Please wait.' }
});

const verifyLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,                   // max 10 verify attempts per minute
  message: { error: 'Too many attempts. Please wait.' }
});

// ── GENERATE CAPTCHA ───────────────────────────────────
app.get('/generate-captcha', generateLimiter, (req, res) => {
  req.session.attempts = 0; // reset attempt counter on new CAPTCHA

  exec('venv311\\Scripts\\python.exe ml/generate.py',
    { cwd: 'C:\\Users\\KIIT\\Desktop\\captcha-project' },
    (error, stdout, stderr) => {
      if (error) {
        return res.status(500).json({ error: 'Failed to generate CAPTCHA' });
      }

      const answer = stdout.trim();
      req.session.captchaAnswer = answer;
      // ✅ answer no longer logged

      res.json({ image: '/generated/captcha.png?t=' + Date.now() });
    });
});

// ── VERIFY CAPTCHA ─────────────────────────────────────
app.post('/verify-captcha', verifyLimiter, (req, res) => {
  const userInput = req.body.answer?.trim();
  const correct   = req.session.captchaAnswer;

  if (!correct) {
    return res.json({ success: false, message: 'CAPTCHA expired. Refresh.' });
  }

  // ── ATTEMPT TRACKING ──────────────────────────────
  req.session.attempts = (req.session.attempts || 0) + 1;

  if (req.session.attempts > 3) {
    req.session.captchaAnswer = null;
    return res.json({
      success: false,
      message: '🔒 Too many wrong attempts. Loading new CAPTCHA.',
      reload: true
    });
  }

  if (userInput === correct) {
    req.session.captchaAnswer = null;
    req.session.attempts = 0;
    res.json({ success: true, message: '✅ Correct! Verification successful.' });
  } else {
    const remaining = 3 - req.session.attempts;
    res.json({
      success: false,
      message: `❌ Wrong CAPTCHA. ${remaining} attempt${remaining === 1 ? '' : 's'} remaining.`
    });
  }
});

// ── START SERVER ───────────────────────────────────────
app.listen(3000, () => {
  console.log('Server running at http://localhost:3000');
});