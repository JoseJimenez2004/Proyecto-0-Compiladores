document.getElementById("crear").addEventListener("click", () => {
  const n = parseInt(document.getElementById("numAut").value);
  const grid = document.getElementById("automasGrid");
  grid.innerHTML = "";

  for (let i = 0; i < n; i++) {
    const cell = document.createElement("div");
    cell.className = "cell";

    const label = document.createElement("label");
    label.textContent = `Autómata ${i + 1}`;

    const input = document.createElement("input");
    input.type = "text";
    input.id = `afn-input-${i}`;
    input.placeholder = "Ingrese expresión";

    const output = document.createElement("div");
    output.id = `afn-output-${i}`;
    output.className = "output";
    output.textContent = "Respuesta aquí...";

    const viewButton = document.createElement("button");
    viewButton.textContent = "Ver autómata";
    viewButton.addEventListener("click", () => {
      const expr = input.value.trim();
      graficarEnModal(expr);
    });

    cell.appendChild(label);
    cell.appendChild(input);
    cell.appendChild(output);
    cell.appendChild(viewButton);
    grid.appendChild(cell);
  }
});

document.getElementById("analizar").addEventListener("click", () => {
  const grid = document.getElementById("automasGrid");
  const inputs = grid.querySelectorAll("input[type='text']");

  inputs.forEach((input, i) => {
    const expression = input.value.trim();
    const output = document.getElementById(`afn-output-${i}`);
    const { operations, steps } = analizarExpresion(expression);

    const result = `Autómata ${i + 1}:\n` +
                   `Operaciones detectadas: ${operations.join(", ")}\n\n` +
                   `Paso a paso:\n${steps.join("\n")}`;

    output.textContent = result;
  });
});

function analizarExpresion(expr) {
  const operations = [];
  const steps = [];
  let count = 1;

  if (expr.includes("|")) {
    operations.push("Unión");
    const parts = expr.split("|");
    steps.push(`[Paso ${count++}] Unión entre: "${parts[0]}" y "${parts.slice(1).join('|')}"`);
  }

  if (expr.includes("&")) {
    operations.push("Concatenación");
    const parts = expr.split("&");
    steps.push(`[Paso ${count++}] Concatenación entre: "${parts.join('" y "')}"`);
  }

  if (expr.includes("+")) {
    operations.push("Cerradura positiva");
    steps.push(`[Paso ${count++}] Cerradura positiva detectada`);
  }

  if (expr.includes("*")) {
    operations.push("Cerradura de Kleene");
    steps.push(`[Paso ${count++}] Cerradura de Kleene detectada`);
  }

  if (expr.includes("?")) {
    operations.push("Cerradura opcional");
    steps.push(`[Paso ${count++}] Cerradura opcional detectada`);
  }

  const basicSymbols = ["(", ")", ".", "@", "-", ">", "[", "]"];
  for (let sym of basicSymbols) {
    if (expr.includes(sym)) {
      operations.push(`Símbolo básico '${sym}'`);
      steps.push(`[Paso ${count++}] Símbolo básico detectado: '${sym}'`);
    }
  }

  if (operations.length === 0) {
    steps.push("[Paso 1] No se detectaron operaciones. Autómata simple.");
  }

  return { operations, steps };
}

// Modal y graficación
const modal = document.getElementById("modal");
const closeModal = document.querySelector(".close");

closeModal.onclick = () => {
  modal.style.display = "none";
};

window.onclick = (event) => {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

function graficarEnModal(expr) {
  const chars = expr.split("");
  const nodes = new vis.DataSet();
  const edges = new vis.DataSet();

  nodes.add({ id: 0, label: "0", color: { background: "#34d399" } });
  let currentId = 1;

  for (let i = 0; i < chars.length; i++) {
    nodes.add({ id: currentId, label: chars[i] });
    edges.add({ from: currentId - 1, to: currentId, label: chars[i], arrows: "to" });
    currentId++;
  }

  nodes.add({ id: currentId, label: "1", color: { background: "#f87171" } });
  edges.add({ from: currentId - 1, to: currentId, arrows: "to" });

  const data = { nodes, edges };
  const options = {
    nodes: { shape: "ellipse", font: { size: 18 } },
    edges: { font: { align: "middle" }, arrows: "to" },
    physics: false
  };

  modal.style.display = "block";
  const container = document.getElementById("graph-container");
  container.innerHTML = "";
  new vis.Network(container, data, options);
}

// Tokenizar
document.getElementById("tokenizar").addEventListener("click", () => {
  const grid = document.getElementById("automasGrid");
  const inputs = grid.querySelectorAll("input[type='text']");
  const tablaContainer = document.getElementById("tabla-token");

  let tableHTML = `
    <table>
      <thead>
        <tr><th>#</th><th>Cadena</th><th>Asignar Token</th></tr>
      </thead>
      <tbody>
  `;

  inputs.forEach((input, index) => {
    const expr = input.value.trim();
    tableHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${expr || "<i>Vacío</i>"}</td>
        <td><input type="number" min="0" id="token-${index}" class="token-input" /></td>
      </tr>
    `;
  });

  tableHTML += `</tbody></table>`;
  tablaContainer.innerHTML = tableHTML;
});

// Guardar tokens
const tokensGuardados = [];

document.getElementById("guardar-token").addEventListener("click", () => {
  const grid = document.getElementById("automasGrid");
  const inputs = grid.querySelectorAll("input[type='text']");
  const tokenInputs = document.querySelectorAll(".token-input");

  tokensGuardados.length = 0;

  tokenInputs.forEach((input, index) => {
    const cadena = inputs[index].value.trim();
    const token = input.value.trim();
    if (cadena && token) {
      tokensGuardados.push({ cadena, token });
    }
  });

  mostrarMensaje("success", "Tokens guardados correctamente.");
});

// Ver tokens guardados
document.getElementById("ver-tokens").addEventListener("click", () => {
  const tabla = document.getElementById("tabla-tokens-guardados");

  if (tokensGuardados.length === 0) {
    tabla.innerHTML = "<p>No hay tokens guardados.</p>";
  } else {
    let html = `
      <table border="1" style="width:100%; border-collapse:collapse;">
        <thead><tr><th>#</th><th>Cadena</th><th>Token</th></tr></thead>
        <tbody>
    `;

    tokensGuardados.forEach((item, idx) => {
      html += `<tr><td>${idx + 1}</td><td>${item.cadena}</td><td>${item.token}</td></tr>`;
    });

    html += "</tbody></table>";
    tabla.innerHTML = html;
  }

  document.getElementById("modal-tokens").style.display = "block";
});

document.querySelector(".close-tokens").addEventListener("click", () => {
  document.getElementById("modal-tokens").style.display = "none";
});

window.addEventListener("click", (event) => {
  if (event.target == document.getElementById("modal-tokens")) {
    document.getElementById("modal-tokens").style.display = "none";
  }
});

function analizarCadena() {
  const cadena = document.getElementById("inputCadena").value.trim();
  const resultadoTabla = document.getElementById("tablaResultado").getElementsByTagName("tbody")[0];
  resultadoTabla.innerHTML = "";

  const definiciones = [
    { regex: /^([a-zA-Z])([a-zA-Z0-9])*$/, token: 10, color: "green" },    // Palabra alfanumérica
    { regex: /^[0-9]+(\.[0-9]+)?$/, token: 20, color: "blue" },             // Número con o sin decimal
    { regex: /^@+$/, token: 30, color: "orange" },                         // Uno o más @
    { regex: /^\($/, token: 40, color: "red" },                            // (
    { regex: /^\)$/, token: 50, color: "red" },                            // )
    { regex: /^\+$/, token: 60, color: "purple" },                         // +
    { regex: /^\*$/, token: 70, color: "brown" },                          // *
    { regex: /^-\&>$/, token: 80, color: "grey" },                         // -&>
    { regex: /^->$/, token: 80, color: "grey" },                          // ->
  ];

  const tokens = [];
  let i = 0;

  const matchToken = (substr) => {
    for (const def of definiciones) {
      if (def.regex.test(substr)) {
        return def;
      }
    }
    return null;
  };

  while (i < cadena.length) {
    let encontrado = false;

    for (let j = cadena.length; j > i; j--) {
      const subcadena = cadena.substring(i, j);
      const tokenDef = matchToken(subcadena);

      if (tokenDef !== null) {
        tokens.push({ lexema: subcadena, token: tokenDef.token, color: tokenDef.color });
        i = j;
        encontrado = true;
        break;
      }
    }

    if (!encontrado) {
      tokens.push({ lexema: cadena[i], token: "DESCONOCIDO", color: "black" });
      i++;
    }
  }

  tokens.forEach(({ lexema, token, color }) => {
    const fila = document.createElement("tr");
    fila.innerHTML = `<td style="color: ${color};">${lexema}</td><td style="color: ${color};">${token}</td>`;
    resultadoTabla.appendChild(fila);
  });
}


// Mensajes estilizados
function mostrarMensaje(tipo, texto) {
  const mensaje = document.getElementById('mensaje');
  mensaje.className = `alert ${tipo}`; // 'success', 'error', 'info'
  mensaje.textContent = texto;
  mensaje.style.display = 'block';

  setTimeout(() => {
    mensaje.style.display = 'none';
  }, 3000);
}

const auts = JSON.parse(localStorage.getItem("automatas") || "[]");
console.log("Autómatas recuperados:", auts);


function mostrarAnimacion() {
  const resultado = [
    { lexema: "2.85", token: 20 },
    { lexema: "+", token: 60 },
    { lexema: "(", token: 40 },
    { lexema: "37", token: 20 },
    { lexema: "+", token: 60 },
    { lexema: "16.2", token: 20 },
    { lexema: ")", token: 50 },
    { lexema: "*", token: 70 },
    { lexema: "27", token: 20 },
    { lexema: "@@@", token: 30 },
    { lexema: "+", token: 60 },
    { lexema: "aZB18", token: 10 },
    { lexema: "@", token: 30 },
    { lexema: "->", token: 80 },
    { lexema: "16.5", token: 20 }
  ];

  const contenedor = document.getElementById("animacion-contenedor");
  contenedor.innerHTML = ""; // limpia contenido previo

  let i = 0;

  function animar() {
    if (i < resultado.length) {
      const span = document.createElement("span");
      span.textContent = resultado[i].lexema;
      span.className = `token-${resultado[i].token}`;
      contenedor.appendChild(span);
      i++;
      setTimeout(animar, 600); // espera entre lexemas
    }
  }

  animar();
}

