/**
 * LIG DNA TODO APP - Frontend Controller
 * Complete Task Management with Realtime Statistics, Filters, Focus Timer & Themes
 */

document.addEventListener('DOMContentLoaded', () => {
  // Application State
  const state = {
    todos: [],
    stats: { total: 0, completed: 0, active: 0, starred: 0, due_today: 0, progress: 0 },
    currentFilter: 'all',
    categoryFilter: 'ALL',
    sortOrder: 'default',
    searchQuery: '',
    editingId: null,
    
    // Focus Timer
    timerDuration: 1500, // 25 min default
    timerRemaining: 1500,
    timerInterval: null,
    timerRunning: false
  };

  // DOM Elements
  const taskList = document.getElementById('taskList');
  const emptyState = document.getElementById('emptyState');
  const addTodoForm = document.getElementById('addTodoForm');
  const taskTitleInput = document.getElementById('taskTitleInput');
  const taskCategorySelect = document.getElementById('taskCategorySelect');
  const taskPrioritySelect = document.getElementById('taskPrioritySelect');
  const taskDueDateInput = document.getElementById('taskDueDateInput');
  const taskStarCheckbox = document.getElementById('taskStarCheckbox');
  const taskDescInput = document.getElementById('taskDescInput');
  const descWrap = document.getElementById('descWrap');
  const toggleDescBtn = document.getElementById('toggleDescBtn');

  // Stats DOM
  const progressPercentBadge = document.getElementById('progressPercentBadge');
  const progressBarFill = document.getElementById('progressBarFill');
  const progressCaption = document.getElementById('progressCaption');
  const statActive = document.getElementById('statActive');
  const statDueToday = document.getElementById('statDueToday');
  const statStarred = document.getElementById('statStarred');
  const statCompleted = document.getElementById('statCompleted');

  // Badges in Tabs
  const badgeAll = document.getElementById('badgeAll');
  const badgeActive = document.getElementById('badgeActive');
  const badgeStarred = document.getElementById('badgeStarred');
  const badgeToday = document.getElementById('badgeToday');
  const badgeCompleted = document.getElementById('badgeCompleted');

  // Filter Controls
  const filterTabs = document.querySelectorAll('.filter-tab');
  const filterCategory = document.getElementById('filterCategory');
  const sortOrder = document.getElementById('sortOrder');
  const searchInput = document.getElementById('searchInput');
  const clearCompletedBtn = document.getElementById('clearCompletedBtn');

  // Modals
  const editModal = document.getElementById('editModal');
  const editTodoForm = document.getElementById('editTodoForm');
  const editTaskId = document.getElementById('editTaskId');
  const editTaskTitle = document.getElementById('editTaskTitle');
  const editTaskCategory = document.getElementById('editTaskCategory');
  const editTaskPriority = document.getElementById('editTaskPriority');
  const editTaskDueDate = document.getElementById('editTaskDueDate');
  const editTaskDesc = document.getElementById('editTaskDesc');
  const closeEditModalBtn = document.getElementById('closeEditModalBtn');
  const cancelEditBtn = document.getElementById('cancelEditBtn');

  // Focus Timer Elements
  const openTimerBtn = document.getElementById('openTimerBtn');
  const timerModal = document.getElementById('timerModal');
  const closeTimerModalBtn = document.getElementById('closeTimerModalBtn');
  const timerDigits = document.getElementById('timerDigits');
  const timerToggleBtn = document.getElementById('timerToggleBtn');
  const timerResetBtn = document.getElementById('timerResetBtn');
  const timerStatusLabel = document.getElementById('timerStatusLabel');
  const timerRingProgress = document.getElementById('timerRingProgress');
  const timerModeBtns = document.querySelectorAll('.mode-btn');

  // Header & Theme
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const exportBtn = document.getElementById('exportBtn');
  const liveClock = document.getElementById('liveClock');
  const toastContainer = document.getElementById('toastContainer');
  const presetChips = document.querySelectorAll('.preset-chip');

  /* ==========================================================================
     Clock & Date Display
     ========================================================================== */
  function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    if (liveClock) {
      liveClock.textContent = `${hours}:${minutes}:${seconds}`;
    }
  }
  setInterval(updateClock, 1000);
  updateClock();

  // Set default due date to today in form
  const todayStr = new Date().toISOString().split('T')[0];
  if (taskDueDateInput) {
    taskDueDateInput.value = todayStr;
  }

  /* ==========================================================================
     Theme Switcher (Dark / Light)
     ========================================================================== */
  const savedTheme = localStorage.getItem('lig_dna_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('lig_dna_theme', next);
      showToast(`${next === 'dark' ? '🌙 다크' : '☀️ 라이트'} 테마로 전환되었습니다.`, 'info');
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

    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  /* ==========================================================================
     API Calls
     ========================================================================== */
  async function loadData() {
    try {
      const [todosRes, statsRes] = await Promise.all([
        fetch('/api/todos'),
        fetch('/api/stats')
      ]);

      const todosData = await todosRes.json();
      const statsData = await statsRes.json();

      if (todosData.status === 'success') {
        state.todos = todosData.todos;
      }
      if (statsData.status === 'success') {
        state.stats = statsData.stats;
      }

      renderStats();
      renderTodos();
    } catch (err) {
      console.error('데이터 로드 실패:', err);
      showToast('서버와의 통신에 실패했습니다.', 'error');
    }
  }

  /* ==========================================================================
     Render Statistics
     ========================================================================== */
  function renderStats() {
    const s = state.stats;
    if (progressPercentBadge) progressPercentBadge.textContent = `${s.progress}%`;
    if (progressBarFill) progressBarFill.style.width = `${s.progress}%`;
    if (progressCaption) progressCaption.textContent = `${s.completed}개 완료됨 / 총 ${s.total}개 업무`;
    if (statActive) statActive.textContent = s.active;
    if (statDueToday) statDueToday.textContent = s.due_today;
    if (statStarred) statStarred.textContent = s.starred;
    if (statCompleted) statCompleted.textContent = s.completed;

    // Badges in Tabs
    if (badgeAll) badgeAll.textContent = s.total;
    if (badgeActive) badgeActive.textContent = s.active;
    if (badgeStarred) badgeStarred.textContent = s.starred;
    if (badgeToday) badgeToday.textContent = s.due_today;
    if (badgeCompleted) badgeCompleted.textContent = s.completed;
  }

  /* ==========================================================================
     Filtering & Sorting
     ========================================================================== */
  function getFilteredAndSortedTodos() {
    const today = new Date().toISOString().split('T')[0];
    
    // 1. Tab Filtering
    let list = state.todos.filter(todo => {
      if (state.currentFilter === 'active') return todo.completed === 0;
      if (state.currentFilter === 'starred') return todo.is_starred === 1 && todo.completed === 0;
      if (state.currentFilter === 'today') return todo.due_date === today && todo.completed === 0;
      if (state.currentFilter === 'completed') return todo.completed === 1;
      return true; // 'all'
    });

    // 2. Category Filtering
    if (state.categoryFilter !== 'ALL') {
      list = list.filter(todo => todo.category === state.categoryFilter);
    }

    // 3. Search Query
    if (state.searchQuery.trim()) {
      const q = state.searchQuery.toLowerCase();
      list = list.filter(todo => 
        (todo.title && todo.title.toLowerCase().includes(q)) ||
        (todo.description && todo.description.toLowerCase().includes(q)) ||
        (todo.category && todo.category.toLowerCase().includes(q))
      );
    }

    // 4. Sorting
    list.sort((a, b) => {
      // Always keep completed at the bottom unless in completed tab
      if (state.currentFilter !== 'completed') {
        if (a.completed !== b.completed) return a.completed - b.completed;
      }

      if (state.sortOrder === 'priority') {
        const pOrder = { '긴급': 1, '높음': 2, '보통': 3, '낮음': 4 };
        return (pOrder[a.priority] || 5) - (pOrder[b.priority] || 5);
      }
      if (state.sortOrder === 'dueAsc') {
        if (!a.due_date) return 1;
        if (!b.due_date) return -1;
        return a.due_date.localeCompare(b.due_date);
      }
      if (state.sortOrder === 'newest') {
        return b.id - a.id;
      }
      // 'default': starred first, then higher id
      if (b.is_starred !== a.is_starred) return b.is_starred - a.is_starred;
      return b.id - a.id;
    });

    return list;
  }

  /* ==========================================================================
     Render Task List
     ========================================================================== */
  function calculateDDay(dueDate) {
    if (!dueDate) return null;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const target = new Date(dueDate);
    target.setHours(0, 0, 0, 0);
    const diffTime = target - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return { label: '오늘 마감', class: 'is-today' };
    if (diffDays < 0) return { label: `D+${Math.abs(diffDays)} 지남`, class: 'is-overdue' };
    return { label: `D-${diffDays}`, class: '' };
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function renderTodos() {
    const filtered = getFilteredAndSortedTodos();
    taskList.innerHTML = '';

    if (filtered.length === 0) {
      emptyState.style.display = 'block';
    } else {
      emptyState.style.display = 'none';

      filtered.forEach(todo => {
        const li = document.createElement('li');
        li.className = `task-card ${todo.completed ? 'is-completed' : ''} ${todo.is_starred ? 'is-starred' : ''}`;
        li.setAttribute('data-id', todo.id);

        const dday = calculateDDay(todo.due_date);
        const hasDesc = todo.description && todo.description.trim().length > 0;

        li.innerHTML = `
          <!-- Custom Checkbox -->
          <label class="check-wrap" title="${todo.completed ? '미완료로 변경' : '완료 처리'}">
            <input type="checkbox" class="check-input" ${todo.completed ? 'checked' : ''} data-id="${todo.id}">
            <span class="check-custom">
              <svg viewBox="0 0 24 24" fill="none">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </span>
          </label>

          <!-- Main Info -->
          <div class="task-content-area">
            <div class="task-meta-top">
              <span class="badge badge-cat-${escapeHtml(todo.category)}">${escapeHtml(todo.category)}</span>
              <span class="badge badge-pri-${escapeHtml(todo.priority)}">${escapeHtml(todo.priority)}</span>
              ${dday ? `<span class="badge badge-due ${dday.class}">📅 ${dday.label} (${escapeHtml(todo.due_date)})</span>` : ''}
              ${todo.completed && todo.completed_at ? `<span class="badge" style="background: rgba(16,185,129,0.1); color: #34d399; font-size: 0.7rem;">완료: ${escapeHtml(todo.completed_at.substring(5, 16))}</span>` : ''}
            </div>
            
            <div class="task-title">${escapeHtml(todo.title)}</div>
            ${hasDesc ? `<div class="task-description">${escapeHtml(todo.description)}</div>` : ''}
          </div>

          <!-- Actions -->
          <div class="task-actions">
            <!-- Star Toggle -->
            <button class="action-icon-btn star-btn ${todo.is_starred ? 'active' : ''}" data-id="${todo.id}" title="${todo.is_starred ? '중요 표시 해제' : '중요 업무 지정'}">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="${todo.is_starred ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
            </button>

            <!-- Edit Button -->
            <button class="action-icon-btn edit-btn" data-id="${todo.id}" title="할 일 수정">
              <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>

            <!-- Delete Button -->
            <button class="action-icon-btn delete-btn" data-id="${todo.id}" title="할 일 삭제">
              <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        `;

        taskList.appendChild(li);
      });
    }
  }

  /* ==========================================================================
     Task Event Delegation
     ========================================================================== */
  taskList.addEventListener('click', async (e) => {
    // 1. Toggle Complete
    const checkInput = e.target.closest('.check-input');
    if (checkInput) {
      const id = checkInput.getAttribute('data-id');
      try {
        const res = await fetch(`/api/todos/${id}/toggle`, { method: 'POST' });
        const data = await res.json();
        if (data.status === 'success') {
          showToast(data.completed ? '할 일을 완료했습니다! 🎉' : '진행 중으로 변경되었습니다.', 'info');
          loadData();
        }
      } catch (err) {
        showToast('상태 변경 실패', 'error');
      }
      return;
    }

    // 2. Toggle Star
    const starBtn = e.target.closest('.star-btn');
    if (starBtn) {
      const id = starBtn.getAttribute('data-id');
      try {
        const res = await fetch(`/api/todos/${id}/star`, { method: 'POST' });
        const data = await res.json();
        if (data.status === 'success') {
          showToast(data.is_starred ? '중요 업무로 등록되었습니다 ⭐' : '중요 업무가 해제되었습니다.', 'info');
          loadData();
        }
      } catch (err) {
        showToast('중요 표시 변경 실패', 'error');
      }
      return;
    }

    // 3. Edit Modal Open
    const editBtn = e.target.closest('.edit-btn');
    if (editBtn) {
      const id = parseInt(editBtn.getAttribute('data-id'), 10);
      const todo = state.todos.find(t => t.id === id);
      if (todo) {
        state.editingId = id;
        editTaskId.value = todo.id;
        editTaskTitle.value = todo.title;
        editTaskCategory.value = todo.category;
        editTaskPriority.value = todo.priority;
        editTaskDueDate.value = todo.due_date || '';
        editTaskDesc.value = todo.description || '';
        editModal.style.display = 'flex';
      }
      return;
    }

    // 4. Delete
    const delBtn = e.target.closest('.delete-btn');
    if (delBtn) {
      const id = delBtn.getAttribute('data-id');
      if (confirm('이 할 일을 삭제하시겠습니까?')) {
        try {
          const res = await fetch(`/api/todos/${id}`, { method: 'DELETE' });
          const data = await res.json();
          if (data.status === 'success') {
            showToast('할 일이 삭제되었습니다.', 'info');
            loadData();
          }
        } catch (err) {
          showToast('삭제 중 오류가 발생했습니다.', 'error');
        }
      }
      return;
    }
  });

  /* ==========================================================================
     Add Todo Form Submit
     ========================================================================== */
  if (addTodoForm) {
    addTodoForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = taskTitleInput.value.trim();
      if (!title) return;

      const payload = {
        title: title,
        category: taskCategorySelect.value,
        priority: taskPrioritySelect.value,
        due_date: taskDueDateInput.value,
        is_starred: taskStarCheckbox.checked,
        description: taskDescInput.value.trim()
      };

      try {
        const res = await fetch('/api/todos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast('새로운 업무가 등록되었습니다! 🚀', 'success');
          // Reset form
          taskTitleInput.value = '';
          taskDescInput.value = '';
          taskStarCheckbox.checked = false;
          descWrap.style.display = 'none';
          loadData();
        } else {
          showToast(data.message || '등록 실패', 'error');
        }
      } catch (err) {
        showToast('등록 중 오류가 발생했습니다.', 'error');
      }
    });
  }

  // Toggle Description Input in Form
  if (toggleDescBtn) {
    toggleDescBtn.addEventListener('click', () => {
      const isHidden = descWrap.style.display === 'none';
      descWrap.style.display = isHidden ? 'block' : 'none';
      toggleDescBtn.textContent = isHidden ? '- 상세 닫기' : '+ 상세 메모';
      if (isHidden) taskDescInput.focus();
    });
  }

  /* ==========================================================================
     Edit Modal Handlers
     ========================================================================== */
  function closeEditModal() {
    editModal.style.display = 'none';
    state.editingId = null;
  }

  if (closeEditModalBtn) closeEditModalBtn.addEventListener('click', closeEditModal);
  if (cancelEditBtn) cancelEditBtn.addEventListener('click', closeEditModal);

  if (editTodoForm) {
    editTodoForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!state.editingId) return;

      const payload = {
        title: editTaskTitle.value.trim(),
        category: editTaskCategory.value,
        priority: editTaskPriority.value,
        due_date: editTaskDueDate.value,
        description: editTaskDesc.value.trim()
      };

      try {
        const res = await fetch(`/api/todos/${state.editingId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.status === 'success') {
          showToast('할 일이 성공적으로 수정되었습니다.', 'success');
          closeEditModal();
          loadData();
        } else {
          showToast(data.message || '수정 실패', 'error');
        }
      } catch (err) {
        showToast('수정 중 오류가 발생했습니다.', 'error');
      }
    });
  }

  /* ==========================================================================
     Filters & Search Listeners
     ========================================================================== */
  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      filterTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      state.currentFilter = tab.getAttribute('data-filter');
      renderTodos();
    });
  });

  if (filterCategory) {
    filterCategory.addEventListener('change', (e) => {
      state.categoryFilter = e.target.value;
      renderTodos();
    });
  }

  if (sortOrder) {
    sortOrder.addEventListener('change', (e) => {
      state.sortOrder = e.target.value;
      renderTodos();
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      renderTodos();
    });
  }

  // Clear completed todos
  if (clearCompletedBtn) {
    clearCompletedBtn.addEventListener('click', async () => {
      if (confirm('완료된 모든 할 일을 목록에서 완전히 삭제하시겠습니까?')) {
        try {
          const res = await fetch('/api/todos/clear-completed', { method: 'POST' });
          const data = await res.json();
          if (data.status === 'success') {
            showToast(`${data.deleted_count}개의 완료된 업무를 정리했습니다.`, 'info');
            loadData();
          }
        } catch (err) {
          showToast('정리 중 오류가 발생했습니다.', 'error');
        }
      }
    });
  }

  /* ==========================================================================
     Preset Quick Task Chips
     ========================================================================== */
  presetChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const title = chip.getAttribute('data-title');
      const cat = chip.getAttribute('data-cat');
      const pri = chip.getAttribute('data-pri');
      
      taskTitleInput.value = title;
      taskCategorySelect.value = cat;
      taskPrioritySelect.value = pri;
      taskDueDateInput.value = todayStr;
      taskTitleInput.focus();
      showToast(`'${title}' 템플릿이 입력창에 적용되었습니다.`, 'info');
    });
  });

  /* ==========================================================================
     Data Export (Backup)
     ========================================================================== */
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      window.location.href = '/api/export';
      showToast('백업 파일 다운로드가 시작되었습니다.', 'success');
    });
  }

  /* ==========================================================================
     Focus Timer (Pomodoro Widget)
     ========================================================================== */
  function updateTimerDisplay() {
    const mins = Math.floor(state.timerRemaining / 60);
    const secs = state.timerRemaining % 60;
    timerDigits.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

    // Ring progress calculation (dasharray is 596.9)
    const max = state.timerDuration;
    const offset = 596.9 - (596.9 * state.timerRemaining / max);
    if (timerRingProgress) {
      timerRingProgress.style.strokeDashoffset = offset;
    }
  }

  function startTimer() {
    state.timerRunning = true;
    timerToggleBtn.textContent = '일시 정지';
    timerToggleBtn.style.background = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)';
    timerStatusLabel.textContent = '집중 진행 중 🔥';

    state.timerInterval = setInterval(() => {
      if (state.timerRemaining > 0) {
        state.timerRemaining--;
        updateTimerDisplay();
      } else {
        pauseTimer();
        timerStatusLabel.textContent = '타이머 완료! 수고하셨습니다 👏';
        showToast('⏰ 설정한 집중 시간이 완료되었습니다! 잠시 스트레칭을 해보세요.', 'success');
        // Visual flash or sound
        try {
          const ctx = new (window.AudioContext || window.webkitAudioContext)();
          const osc = ctx.createOscillator();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
          osc.connect(ctx.destination);
          osc.start();
          osc.stop(ctx.currentTime + 0.4);
        } catch (e) {}
      }
    }, 1000);
  }

  function pauseTimer() {
    state.timerRunning = false;
    clearInterval(state.timerInterval);
    timerToggleBtn.textContent = '계속 진행';
    timerToggleBtn.style.background = 'var(--dna-gradient)';
    timerStatusLabel.textContent = '일시 정지됨';
  }

  function resetTimer() {
    pauseTimer();
    state.timerRemaining = state.timerDuration;
    timerToggleBtn.textContent = '시작';
    timerStatusLabel.textContent = '준비 완료';
    updateTimerDisplay();
  }

  if (openTimerBtn) {
    openTimerBtn.addEventListener('click', () => {
      timerModal.style.display = 'flex';
      updateTimerDisplay();
    });
  }

  if (closeTimerModalBtn) {
    closeTimerModalBtn.addEventListener('click', () => {
      timerModal.style.display = 'none';
    });
  }

  if (timerToggleBtn) {
    timerToggleBtn.addEventListener('click', () => {
      if (state.timerRunning) {
        pauseTimer();
      } else {
        startTimer();
      }
    });
  }

  if (timerResetBtn) {
    timerResetBtn.addEventListener('click', resetTimer);
  }

  timerModeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      timerModeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const time = parseInt(btn.getAttribute('data-time'), 10);
      state.timerDuration = time;
      state.timerRemaining = time;
      resetTimer();
    });
  });

  // Modal Backdrop Close & ESC key
  window.addEventListener('click', (e) => {
    if (e.target === editModal) closeEditModal();
    if (e.target === timerModal) timerModal.style.display = 'none';
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (editModal.style.display === 'flex') closeEditModal();
      if (timerModal.style.display === 'flex') timerModal.style.display = 'none';
    }
  });

  // Initial Load
  loadData();
});
