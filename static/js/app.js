/**
 * 오늘 뭐먹지? - Frontend Controller
 * Restaurant Recommendation: Condition Form, AJAX Recommendation, Result Cards
 */

document.addEventListener('DOMContentLoaded', () => {
  const state = {
    foodType: '상관없음',
    moods: [],
    isLoading: false
  };

  // DOM Elements
  const recommendForm = document.getElementById('recommendForm');
  const locationInput = document.getElementById('locationInput');
  const regionChips = document.querySelectorAll('#regionChips .preset-chip');
  const foodTypeGroup = document.querySelectorAll('#foodTypeGroup .chip-select');
  const budgetSelect = document.getElementById('budgetSelect');
  const peopleSelect = document.getElementById('peopleSelect');
  const moodGroup = document.querySelectorAll('#moodGroup .chip-select');
  const requestTextarea = document.getElementById('requestTextarea');
  const formError = document.getElementById('formError');
  const recommendBtn = document.getElementById('recommendBtn');
  const recommendBtnText = document.getElementById('recommendBtnText');

  const loadingState = document.getElementById('loadingState');
  const resultSection = document.getElementById('resultSection');
  const resultHeading = document.getElementById('resultHeading');
  const restaurantGrid = document.getElementById('restaurantGrid');
  const emptyState = document.getElementById('emptyState');

  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const toastContainer = document.getElementById('toastContainer');

  /* ==========================================================================
     Theme Switcher (Dark / Light)
     ========================================================================== */
  const savedTheme = localStorage.getItem('food_finder_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('food_finder_theme', next);
    });
  }

  /* ==========================================================================
     Toast Notifications
     ========================================================================== */
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let icon = '✓';
    if (type === 'error') icon = '✕';
    if (type === 'info') icon = 'ℹ';

    toast.innerHTML = `<span>${icon}</span> <span>${escapeHtml(message)}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /* ==========================================================================
     Region Quick Chips -> fill location input
     ========================================================================== */
  regionChips.forEach(chip => {
    chip.addEventListener('click', () => {
      locationInput.value = chip.getAttribute('data-value');
      locationInput.focus();
    });
  });

  /* ==========================================================================
     Food Type (single select) & Mood (multi select) chip groups
     ========================================================================== */
  foodTypeGroup.forEach(btn => {
    btn.addEventListener('click', () => {
      foodTypeGroup.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.foodType = btn.getAttribute('data-value');
    });
  });

  moodGroup.forEach(btn => {
    btn.addEventListener('click', () => {
      const value = btn.getAttribute('data-value');
      btn.classList.toggle('active');
      if (btn.classList.contains('active')) {
        state.moods.push(value);
      } else {
        state.moods = state.moods.filter(m => m !== value);
      }
    });
  });

  /* ==========================================================================
     Result Card Rendering
     ========================================================================== */
  function foodTypeEmoji(foodType) {
    const map = {
      '한식': '🍚', '중식': '🥢', '일식': '🍣', '양식': '🍝',
      '치킨': '🍗', '고기': '🥩', '카페': '☕', '디저트': '🍰'
    };
    return map[foodType] || '🍽️';
  }

  function renderResults(results) {
    restaurantGrid.innerHTML = '';

    results.forEach((r, idx) => {
      const card = document.createElement('div');
      card.className = 'restaurant-card';
      card.innerHTML = `
        <div class="card-top-row">
          <div class="card-name">${foodTypeEmoji(r.food_type)} ${escapeHtml(r.name)}</div>
          <div class="card-rating">⭐ ${escapeHtml(r.rating)}</div>
        </div>
        <div class="card-meta">${escapeHtml(r.cuisine)} · ${escapeHtml(r.region)} · 리뷰 ${escapeHtml(r.review_count)}개</div>
        <div class="card-price">💰 ${escapeHtml(r.price_display)}</div>
        <div class="card-reason">"${escapeHtml(r.reason)}"</div>
        <div class="card-detail" id="detail-${idx}">
          <span>🍴 대표메뉴: ${escapeHtml(r.signature_menu)}</span>
          <span>📍 ${escapeHtml(r.address)}</span>
          <span>🕒 ${escapeHtml(r.hours)}</span>
        </div>
        <div class="card-actions">
          <a class="card-action-btn" target="_blank" rel="noopener noreferrer"
             href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(r.map_query)}">지도 보기</a>
          <button type="button" class="card-action-btn detail-toggle-btn" data-target="detail-${idx}">상세보기</button>
        </div>
      `;
      restaurantGrid.appendChild(card);
    });

    restaurantGrid.querySelectorAll('.detail-toggle-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const target = document.getElementById(btn.getAttribute('data-target'));
        if (target) {
          target.classList.toggle('open');
          btn.textContent = target.classList.contains('open') ? '접기' : '상세보기';
        }
      });
    });
  }

  /* ==========================================================================
     Form Submit -> POST /api/recommend
     ========================================================================== */
  function setLoading(isLoading) {
    state.isLoading = isLoading;
    recommendBtn.disabled = isLoading;
    recommendBtnText.textContent = isLoading ? '추천을 찾는 중...' : '🍽️ 맛집 추천받기';
    loadingState.style.display = isLoading ? 'block' : 'none';
    if (isLoading) {
      resultSection.style.display = 'none';
      emptyState.style.display = 'none';
    }
  }

  function showFormError(message) {
    formError.textContent = message;
    formError.style.display = 'block';
  }

  function clearFormError() {
    formError.style.display = 'none';
    formError.textContent = '';
  }

  if (recommendForm) {
    recommendForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (state.isLoading) return;

      clearFormError();
      const location = locationInput.value.trim();
      const foodType = state.foodType;

      if (!location && (!foodType || foodType === '상관없음')) {
        showFormError('지역 또는 원하는 음식 종류를 입력해주세요.');
        return;
      }

      const payload = {
        location: location,
        food_type: foodType,
        budget: budgetSelect.value,
        people: peopleSelect.value,
        mood: state.moods,
        request: requestTextarea.value.trim()
      };

      setLoading(true);

      try {
        const res = await fetch('/api/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        let data;
        try {
          data = await res.json();
        } catch (parseErr) {
          throw new Error('invalid_response');
        }

        setLoading(false);

        if (!res.ok || data.status !== 'success') {
          showFormError(data.message || '맛집 정보를 가져오는 중 문제가 발생했습니다.\n잠시 후 다시 시도해주세요.');
          return;
        }

        if (!data.results || data.results.length === 0) {
          resultSection.style.display = 'none';
          emptyState.style.display = 'block';
          return;
        }

        emptyState.style.display = 'none';
        resultHeading.textContent = `추천 결과 (${data.results.length}곳)`;
        renderResults(data.results);
        resultSection.style.display = 'block';
      } catch (err) {
        setLoading(false);
        showFormError('맛집 정보를 가져오는 중 문제가 발생했습니다.\n잠시 후 다시 시도해주세요.');
        showToast('추천을 생성하지 못했습니다.', 'error');
      }
    });
  }
});
