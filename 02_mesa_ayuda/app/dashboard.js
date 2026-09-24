const BASE_TICKETS = [
  {
    id: "INC-1001",
    title: "No es posible conectar con la VPN",
    requester: "maria.solicitante",
    requesterName: "María López",
    priority: "Media",
    group: "Mesa de ayuda",
    status: "ABIERTO",
    description: "La conexión se interrumpe después de validar las credenciales.",
  },
  {
    id: "INC-1002",
    title: "Impresora sin conexión",
    requester: "maria.solicitante",
    requesterName: "María López",
    priority: "Baja",
    group: "Infraestructura",
    status: "RESUELTO",
    description: "La impresora del área administrativa no aparece disponible.",
  },
  {
    id: "INC-1003",
    title: "Acceso denegado al sistema de nómina",
    requester: "carlos.usuario",
    requesterName: "Carlos Pérez",
    priority: "Alta",
    group: "Aplicaciones",
    status: "EN_PROCESO",
    description: "El usuario recibe un mensaje de permisos insuficientes.",
  },
];

const session = JSON.parse(localStorage.getItem("helpdesk.session") || "null");
if (!session) {
  window.location.replace("login.html");
  throw new Error("Sesión no disponible; redirigiendo al acceso.");
}

const overrides = JSON.parse(localStorage.getItem("helpdesk.ticketOverrides") || "{}");
let tickets = BASE_TICKETS.map((ticket) => ({ ...ticket, ...(overrides[ticket.id] || {}) }));
let currentTicket = null;

const byId = (id) => document.getElementById(id);
const statusLabel = (status) => ({
  ABIERTO: "Abierto",
  EN_PROCESO: "En proceso",
  RESUELTO: "Resuelto",
}[status]);

byId("session-name").textContent = session.name;
byId("session-role").textContent = session.role === "AGENTE" ? "Agente" : "Solicitante";
byId("dashboard-description").textContent = session.role === "AGENTE"
  ? "Administre la prioridad, asignación y estado de las incidencias."
  : "Consulte el estado de las incidencias registradas a su nombre.";

function visibleTickets() {
  const permitted = session.role === "AGENTE"
    ? tickets
    : tickets.filter((ticket) => ticket.requester === session.username);
  const filter = byId("status-filter").value;
  return filter === "TODOS" ? permitted : permitted.filter((ticket) => ticket.status === filter);
}

function renderTickets() {
  const list = byId("ticket-list");
  const visible = visibleTickets();
  list.replaceChildren();
  byId("ticket-count").textContent = visible.length;

  if (!visible.length) {
    list.innerHTML = '<p class="empty">No hay tickets con este filtro.</p>';
    return;
  }

  visible.forEach((ticket) => {
    const article = document.createElement("article");
    article.className = "ticket-item";
    article.dataset.ticketId = ticket.id;
    article.innerHTML = `
      <div>
        <span class="ticket-id">${ticket.id}</span>
        <h3>${ticket.title}</h3>
        <p>${ticket.requesterName} · ${ticket.priority}</p>
      </div>
      <div class="ticket-actions">
        <span class="status status-${ticket.status.toLowerCase()}">${statusLabel(ticket.status)}</span>
        <button class="secondary open-ticket" aria-label="Abrir ${ticket.id}">Abrir</button>
      </div>`;
    article.querySelector("button").addEventListener("click", () => showTicket(ticket.id));
    list.appendChild(article);
  });
}

function showTicket(ticketId) {
  currentTicket = tickets.find((ticket) => ticket.id === ticketId);
  byId("ticket-detail").classList.remove("hidden");
  byId("detail-id").textContent = currentTicket.id;
  byId("detail-title").textContent = currentTicket.title;
  byId("detail-status").textContent = statusLabel(currentTicket.status);
  byId("detail-status").className = `status status-${currentTicket.status.toLowerCase()}`;
  byId("detail-requester").textContent = currentTicket.requesterName;
  byId("detail-priority").textContent = currentTicket.priority;
  byId("detail-group").textContent = currentTicket.group;
  byId("detail-description").textContent = currentTicket.description;
  byId("update-message").classList.add("hidden");

  if (session.role === "AGENTE") {
    byId("agent-form").classList.remove("hidden");
    byId("priority").value = currentTicket.priority;
    byId("group").value = currentTicket.group;
    byId("status").value = currentTicket.status;
  } else {
    byId("agent-form").classList.add("hidden");
  }
}

byId("agent-form").addEventListener("submit", (event) => {
  event.preventDefault();
  if (!currentTicket || session.role !== "AGENTE") return;
  const change = {
    priority: byId("priority").value,
    group: byId("group").value,
    status: byId("status").value,
  };
  overrides[currentTicket.id] = change;
  localStorage.setItem("helpdesk.ticketOverrides", JSON.stringify(overrides));
  tickets = tickets.map((ticket) => ticket.id === currentTicket.id ? { ...ticket, ...change } : ticket);
  showTicket(currentTicket.id);
  renderTickets();
  byId("update-message").textContent = `Cambios guardados para ${currentTicket.id}.`;
  byId("update-message").classList.remove("hidden");
});

byId("status-filter").addEventListener("change", renderTickets);
byId("logout").addEventListener("click", () => {
  localStorage.removeItem("helpdesk.session");
  document.cookie = "helpdesk_role=; Max-Age=0; path=/";
  window.location.assign("login.html");
});

renderTickets();
