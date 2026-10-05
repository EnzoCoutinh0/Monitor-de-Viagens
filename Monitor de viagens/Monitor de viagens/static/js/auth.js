// Linha 1: Define uma função de seta para executar a lógica indicada.
(() => {
  // Linha 2: Declara uma constante que não será reatribuída.
  const password = document.getElementById("loginSenha");
  // Linha 3: Declara uma constante que não será reatribuída.
  const toggle = document.getElementById("toggleSenha");
  // Linha 4: Verifica uma condição antes de executar a lógica seguinte.
  if (!password || !toggle) return;

  // Linha 6: Define uma função de seta para executar a lógica indicada.
  toggle.addEventListener("click", () => {
    // Linha 7: Declara uma constante que não será reatribuída.
    const showing = password.type === "password";
    // Linha 8: Executa a instrução JavaScript desta linha.
    password.type = showing ? "text" : "password";
    // Linha 9: Adiciona, remove ou verifica classes CSS de um elemento.
    toggle.classList.toggle("is-visible", showing);
    // Linha 10: Executa a instrução JavaScript desta linha.
    toggle.setAttribute("aria-pressed", String(showing));
    // Linha 11: Executa a instrução JavaScript desta linha.
    toggle.setAttribute("aria-label", showing ? "Ocultar senha" : "Mostrar senha");
    // Linha 12: Executa a instrução JavaScript desta linha.
    toggle.setAttribute("title", showing ? "Ocultar senha" : "Mostrar senha");
  // Linha 13: Executa a instrução JavaScript desta linha.
  });
// Linha 14: Executa a instrução JavaScript desta linha.
})();
