const quickScan = config.quick_scan || [];
document.querySelectorAll(".quick-scan-question").forEach((card, questionIndex) => {
  const savedChoice = data[`quick_${questionIndex}`];
  const feedback = card.querySelector(".quick-scan-feedback");
  const renderChoice = choiceIndex => {
    card.querySelectorAll("button").forEach((button, optionIndex) => {
      button.classList.toggle("selected", optionIndex === choiceIndex);
      button.setAttribute("aria-pressed", optionIndex === choiceIndex ? "true" : "false");
    });
    feedback.textContent = quickScan[questionIndex].options[choiceIndex].feedback;
    feedback.hidden = false;
  };
  card.querySelectorAll("button").forEach((button, optionIndex) => {
    button.addEventListener("click", () => {
      data[`quick_${questionIndex}`] = optionIndex;
      save();
      renderChoice(optionIndex);
    });
  });
  if (savedChoice === 0 || savedChoice === 1) renderChoice(savedChoice);
});
