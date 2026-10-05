(() => {
  const password = document.getElementById("loginSenha");
  const toggle = document.getElementById("toggleSenha");
  if (!password || !toggle) return;

  toggle.addEventListener("click", () => {
    const showing = password.type === "password";
    password.type = showing ? "text" : "password";
    toggle.classList.toggle("is-visible", showing);
    toggle.setAttribute("aria-pressed", String(showing));
    toggle.setAttribute("aria-label", showing ? "Ocultar senha" : "Mostrar senha");
    toggle.setAttribute("title", showing ? "Ocultar senha" : "Mostrar senha");
  });
})();
