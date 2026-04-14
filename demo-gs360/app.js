// Navigation Router
const navItems = document.querySelectorAll('.sidebar-item[data-view]');
const views = document.querySelectorAll('.view');
const progLabel = document.getElementById('progLabel');
const pb = document.getElementById('pb');
const toast = document.getElementById('toast');
const toastMsg = document.getElementById('toastMsg');

navItems.forEach(item => {
  item.onclick = (e) => {
    e.preventDefault();
    const target = item.getAttribute('data-view');

    navItems.forEach(i => i.classList.remove('active'));
    item.classList.add('active');

    views.forEach(v => v.classList.remove('active'));
    const targetView = document.getElementById(`view-${target}`);
    if (targetView) targetView.classList.add('active');
    
    // UI Progress Updates based on Context
    if (target === 'command') {
      progLabel.innerText = 'Milestone: 33.33%';
      pb.style.width = '33.33%';
    } else if (target === 'learning') {
      progLabel.innerText = 'Daily Prep: 66.66%';
      pb.style.width = '66.66%';
    } else if (target === 'dashboard') {
      progLabel.innerText = 'Overall Readiness: 58%';
      pb.style.width = '58%';
    }

    showToast(`Loading ${target.charAt(0).toUpperCase() + target.slice(1)} Engine...`);
  };
});

function showToast(msg) {
    if (!toast) return;
    toastMsg.innerText = msg;
    toast.style.display = 'flex';
    setTimeout(() => { toast.style.display = 'none'; }, 3000);
}

// AI Scoring Simulation
const subBtn = document.getElementById('subBtn');
if (subBtn) {
    subBtn.onclick = () => {
        subBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Quality...';
        subBtn.disabled = true;
        setTimeout(() => {
            subBtn.innerHTML = 'AI Feedback Received!';
            subBtn.classList.add('completed');
            showToast("Mission 2 Done! +200 XP Added.");
            setTimeout(triggerCall, 2000);
        }, 2500);
    };
}

// 3D Flashcard Flip Logic
function flipCard() {
    const cardInner = document.getElementById('cardInner');
    if (cardInner) {
        cardInner.classList.toggle('flipped');
        if (cardInner.classList.contains('flipped')) {
            showToast("Concept Recalled! +10 XP");
        }
    }
}

// Voice Call Overlay
const callOverlay = document.getElementById('callOverlay');
function triggerCall() {
    if (!callOverlay) return;
    callOverlay.style.display = 'flex';
    // Ringtone logic (simplified for mockup)
    console.log("Incoming Strategy Call from AI Mentor...");
}

function declineCall() { callOverlay.style.display = 'none'; showToast("Mentor Call Snoozed."); }
function acceptCall() {
    callOverlay.innerHTML = `
        <div style="text-align:center;">
            <div class="caller-avatar" style="overflow:hidden; border-radius:50%; width:100px; height:100px; margin:0 auto 20px;">
                <img src="https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <h2>Rahul (AI Mentor) Connected</h2>
            <div class="voice-wave" style="display:flex; justify-content:center; gap:4px; margin:20px 0;">
                <div class="wave-bar" style="height:20px; width:4px; background:white; animation: wave 1s infinite"></div>
                <div class="wave-bar" style="height:40px; width:4px; background:white; animation: wave 0.5s infinite"></div>
                <div class="wave-bar" style="height:30px; width:4px; background:white; animation: wave 0.7s infinite"></div>
            </div>
            <p style="padding:0 20px;">"Rahul, your analysis of RBI's liquidity management missed the 'Open Market Operations' angle. Let's fix that now..."</p>
            <button class="call-btn decline" onclick="declineCall()" style="margin-top:40px;"><i class="fa-solid fa-phone-slash"></i></button>
        </div>
    `;
}

// Dashboard Animation
const mainScore = document.getElementById('mainScore');
if (mainScore) {
    let score = 42;
    const interval = setInterval(() => {
        if (score >= 58) clearInterval(interval);
        mainScore.innerText = score;
        score++;
    }, 30);
}

// Bot Control
function toggleBot() { document.getElementById('bot').classList.toggle('active'); }
function startVoice() { showToast("AI is listening..."); }
