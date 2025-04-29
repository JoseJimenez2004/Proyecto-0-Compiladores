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
      steps.push(`[Paso ${count++}] Se detecta una unión entre: "${parts[0]}" y "${parts.slice(1).join('|')}"`);
    }
  
    if (expr.includes("&")) {
      operations.push("Concatenación");
      const parts = expr.split("&");
      steps.push(`[Paso ${count++}] Se detecta una concatenación entre: "${parts.join('" y "')}"`);
    }
  
    if (expr.includes("+")) {
      operations.push("Cerradura positiva");
      steps.push(`[Paso ${count++}] Se detecta una cerradura positiva (uno o más repeticiones)`);
    }
  
    if (expr.includes("*")) {
      operations.push("Cerradura de Kleene");
      steps.push(`[Paso ${count++}] Se detecta una cerradura de Kleene (cero o más repeticiones)`);
    }
  
    if (expr.includes("?")) {
      operations.push("Cerradura opcional");
      steps.push(`[Paso ${count++}] Se detecta una cerradura opcional (una o ninguna aparición)`);
    }
  
    const basicSymbols = ["(", ")", ".", "@", "-", ">", "[", "]"];
    for (let sym of basicSymbols) {
      if (expr.includes(sym)) {
        operations.push(`Símbolo básico '${sym}'`);
        steps.push(`[Paso ${count++}] Símbolo básico detectado: '${sym}'`);
      }
    }
  
    if (operations.length === 0) {
      steps.push("[Paso 1] No se detectaron operaciones. Se trata de un autómata simple.");
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
      nodes: {
        shape: "ellipse",
        font: { size: 18 }
      },
      edges: {
        font: { align: "middle" },
        arrows: "to"
      },
      physics: false
    };
  
    modal.style.display = "block";
    const container = document.getElementById("graph-container");
    container.innerHTML = ""; // limpiar grafo anterior
    new vis.Network(container, data, options);
  }
  