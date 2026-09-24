const USERS = {
  "maria.solicitante": {
    password: "rpa123",
    name: "María López",
    role: "SOLICITANTE",
  },
  "ana.agente": {
    password: "soporte123",
    name: "Ana Torres",
    role: "AGENTE",
  },
};

const form = document.querySelector("#login-form");
const errorBox = document.querySelector("#login-error");

if (localStorage.getItem("helpdesk.session")) {
  window.location.replace("dashboard.html");
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const username = data.get("username").trim();
  const password = data.get("password");
  const account = USERS[username];

  if (!account || account.password !== password) {
    errorBox.textContent = "Credenciales incorrectas. Verifique el usuario y la contraseña.";
    errorBox.classList.remove("hidden");
    return;
  }

  const session = { username, name: account.name, role: account.role };
  localStorage.setItem("helpdesk.session", JSON.stringify(session));
  document.cookie = `helpdesk_role=${account.role}; path=/; SameSite=Lax`;
  window.location.assign("dashboard.html");
});
