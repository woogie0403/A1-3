// ==========================================================================
// 트립스케치 (TripSketch) 프론트엔드 인터랙션 스크립트
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  // DOM 요소 참조
  const form = document.getElementById("travel-form");
  const destinationInput = document.getElementById("destination");
  const durationSelect = document.getElementById("duration");
  const companionSelect = document.getElementById("companion");
  const transportSelect = document.getElementById("transport");
  const errorBox = document.getElementById("error-box");
  const errorMessage = document.getElementById("error-message");
  const loadingBox = document.getElementById("loading-box");
  const loadingDesc = document.getElementById("loading-desc");
  const resultBox = document.getElementById("result-box");
  const chipButtons = document.querySelectorAll(".chip-btn");
  const categoryItems = document.querySelectorAll(".category-item");
  const resetBtn = document.getElementById("reset-btn");
  const copyBtn = document.getElementById("copy-btn");

  // 현재 선택된 테마 (기본: 힐링·자연)
  let currentTheme = "🌿 힐링·자연";

  // 1. 에어비앤비 스타일 가로 카테고리 탭 클릭 이벤트
  categoryItems.forEach((item) => {
    item.addEventListener("click", () => {
      categoryItems.forEach((c) => c.classList.remove("active"));
      item.classList.add("active");
      currentTheme = item.getAttribute("data-theme");
      console.log("선택된 테마:", currentTheme);
    });
  });

  // 2. 인기 추천 여행지 퀵 태그 클릭 이벤트
  chipButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const dest = btn.getAttribute("data-dest");
      destinationInput.value = dest;
      clearError();
      destinationInput.focus();
    });
  });

  // 3. 에러 표시 및 해제 헬퍼 함수
  function showError(msg) {
    errorMessage.textContent = msg;
    errorBox.classList.remove("hidden");
    destinationInput.focus();
  }

  function clearError() {
    errorMessage.textContent = "";
    errorBox.classList.add("hidden");
  }

  // 4. 검색 폼 제출 유효성 검사 및 핸들러 (STEP 5에서 백엔드 API 연동)
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearError();

    const destination = destinationInput.value.trim();
    const duration = durationSelect.value;
    const companion = companionSelect.value;
    const transport = transportSelect.value;

    // [과제 필수 요구사항: 빈 입력값 실패 처리 검증]
    if (!destination) {
      showError("어디로 떠나실지 여행지 이름을 입력해 주세요! (예: 제주도, 강릉, 도쿄)");
      return;
    }

    // [Edge Case 장난 방어: 안방, 화성 등]
    if (["안방", "내방", "우리집", "화성", "달나라", "명왕성"].includes(destination)) {
      showError("아직 지구 밖이나 집 안 여행은 지원하지 않아요! 멋진 지구별 여행지를 입력해 주세요 🚀");
      return;
    }

    // 로딩 UI 활성화 및 맞춤 문구 출력
    loadingDesc.textContent = `${companion}과(와) 함께하는 [${transport}] 최적 동선 및 직전 스팟 반경 10분 이내 맛집을 계산 중입니다 (약 3~7초 소요).`;
    loadingBox.classList.remove("hidden");
    resultBox.classList.add("hidden");

    // 플래너 섹션으로 스크롤
    document.getElementById("planner").scrollIntoView({ behavior: "smooth" });

    console.log("요청 파라미터:", {
      destination,
      duration,
      companion,
      transport,
      theme: currentTheme,
    });
  });

  // 5. 새로 계획하기 버튼
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      resultBox.classList.add("hidden");
      destinationInput.value = "";
      clearError();
      destinationInput.focus();
      document.getElementById("hero").scrollIntoView({ behavior: "smooth" });
    });
  }

  // 6. 전체 일정 복사하기 버튼
  if (copyBtn) {
    copyBtn.addEventListener("click", () => {
      const title = document.getElementById("res-title").innerText;
      const summary = document.getElementById("res-summary").innerText;
      const budget = document.getElementById("res-budget").innerText;
      const tips = document.getElementById("res-tips").innerText;
      const textToCopy = `[트립스케치 AI 맞춤 여행 일정표]\n\n✈️ ${title}\n${summary}\n\n💰 1인 예상 경비: ${budget}\n\n💡 AI 가이드 꿀팁: ${tips}\n\n✨ 트립스케치(TripSketch)에서 생성됨`;

      navigator.clipboard.writeText(textToCopy).then(() => {
        alert("일정이 클립보드에 복사되었습니다! 친구나 연인에게 공유해 보세요. 📋");
      }).catch(() => {
        alert("클립보드 복사 실패: 텍스트를 직접 드래그해 복사해 주세요.");
      });
    });
  }
});
