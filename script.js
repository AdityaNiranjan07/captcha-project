window.onload = loadCaptcha;

function loadCaptcha() {
  const img = document.getElementById('captcha-img');
  const msg = document.getElementById('message');

  img.src = '';
  msg.textContent = 'Generating CAPTCHA...';
  msg.className = 'message';

  fetch('/generate-captcha')
    .then(res => {
      if (res.status === 429) {
        msg.textContent = '⏳ Too many requests. Please wait a minute.';
        msg.className = 'message error';
        return null;
      }
      return res.json();
    })
    .then(data => {
      if (!data) return;
      if (data.image) {
        img.src = data.image;
        msg.textContent = '';
      } else {
        msg.textContent = '❌ Failed to load CAPTCHA';
        msg.className = 'message error';
      }
    })
    .catch(() => {
      msg.textContent = '❌ Server error';
      msg.className = 'message error';
    });

  document.getElementById('captcha-input').value = '';
}

function verifyCaptcha() {
  const input = document.getElementById('captcha-input').value.trim();
  const msg   = document.getElementById('message');

  if (input.length !== 5) {
    msg.textContent = '⚠️ Please enter all 5 digits';
    msg.className = 'message error';
    return;
  }

  fetch('/verify-captcha', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answer: input })
  })
    .then(res => {
      if (res.status === 429) {
        msg.textContent = '⏳ Too many attempts. Please wait a minute.';
        msg.className = 'message error';
        return null;
      }
      return res.json();
    })
    .then(data => {
      if (!data) return;
      msg.textContent = data.message;
      msg.className = data.success ? 'message success' : 'message error';

      if (data.reload || !data.success) {
        setTimeout(loadCaptcha, 1500);
      }
    });
}