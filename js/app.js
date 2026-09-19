// ==========================================================================
// 트립스케치 (TripSketch) 프론트엔드 로직
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  // DOM 요소 참조
  const form = document.getElementById("travel-form");
  const destinationInput = document.getElementById("destination");
  const durationSelect = document.getElementById("duration");
  const errorBox = document.getElementById("error-box");
  const errorMessage = document.getElementById("error-message");
  const loadingBox = document.getElementById("loading-box");
  const resultBox = document.getElementById("result-box");
  const tagButtons = document.querySelectorAll(".tag-btn");
  const resetBtn = document.getElementById("reset-btn");
  const copyBtn = document.getElementById("copy-btn");

  // 1. 추천 여행지 퀵 태그 클릭 이벤트
  tagButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const dest = btn.getAttribute("data-dest");
      destinationInput.value = dest;
      clearError();
      destinationInput.focus();
      // 플래너 섹션으로 부드럽게 스크롤
      document.getElementById("planner").scrollIntoView({ behavior: "smooth" });
    });
  });

  // 2. 에러 표시 및 해제 헬퍼 함수
  function showError(msg) {
    errorMessage.textContent = msg;
    errorBox.classList.remove("hidden");
    destinationInput.focus();
  }

  function clearError() {
    errorMessage.textContent = "";
    errorBox.classList.add("hidden");
  }

  // 3. 폼 제출 유효성 검사 및 핸들러 (STEP 5에서 백엔드 API 연동)
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearError();

    const destination = destinationInput.value.trim();
    const duration = durationSelect.value;
    const selectedTheme = document.querySelector('input[name="theme"]:checked')?.value || "힐링·자연";

    // [과제 필수 요구사항: 빈 입력값 실패 처리 검증]
    if (!destination) {
      showError("어디로 떠나실지 여행지 이름을 입력해 주세요! (예: 제주도, 강릉, 도쿄)");
      return;
    }

    // 로딩 UI 활성화
    loadingBox.classList.remove("hidden");
    resultBox.classList.add("hidden");

    // 다음 STEP(백엔드 구현 및 연동)에서 실제 fetch('/api/generate') 호출을 연결합니다.
    console.log("요청 데이터:", { destination, duration, theme: selectedTheme });
  });

  // 4. 새로 계획하기 버튼
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      resultBox.classList.add("hidden");
      destinationInput.value = "";
      clearError();
      destinationInput.focus();
    });
  }

  // 5. 일정 복사하기 버튼
  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      const title = document.getElementById("res-title").innerText;
      const summary = document.getElementById("res-summary").innerText;
      const tips = document.getElementById("res-tips").innerText;
      const textToCopy = `[트립스케치 AI 여행 일정표]\n\n📌 ${title}\n${summary}\n\n💡 꿀팁: ${tips}\n\n✨ 트립스케치에서 생성됨`;

      navigator.clipboard.writeText(textToCopy).then(() => {
        alert("일정이 클립보드에 복사되었습니다! 친구에게 공유해 보세요. 📋");
      }).catch(() => {
        alert("복사에 실패했습니다. 텍스트를 직접 드래그해 복사해 주세요.");
      });
    });
  }
});
