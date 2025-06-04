function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function verificarLinea(linea) {
  // Validar que la línea tenga la forma: NoTerminal → producción(s)
  const regexProduccion = /^([A-Z][0-9']*)\s*(→|->|=)\s*(.+)$/;
  const regexCuerpo = /^([^|]+)(\s*\|\s*[^|]+)*$/;

  const match = regexProduccion.exec(linea);
  if (!match) return false;

  const cuerpo = match[3].trim();
  return regexCuerpo.test(cuerpo);
}

// Variables globales para la gramática
const producciones = [];
const first = {};
const follow = {};
const simbolos = new Set();

function parsearGramatica(texto) {
  producciones.length = 0; // limpiar array antes de llenar
  simbolos.clear?.(); // Si el Set tiene clear (en navegadores modernos)
  // si no, creamos nuevo:
  if (!simbolos.clear) {
    while (simbolos.size) simbolos.delete(simbolos.values().next().value);
  }

  if (!texto.trim()) return;

  const lineas = texto.split("\n");
  for (const linea of lineas) {
    const clean = linea.trim();
    if (!clean) continue;

    const partes = clean.split(/→|->|=/);
    if (partes.length < 2) continue;

    const ladoIzq = partes[0].trim();
    const ladoDer = partes.slice(1).join("=").trim(); // en caso de que haya "=" dentro de la producción
    const opciones = ladoDer.split("|").map(p => p.trim().split(/\s+/));
    producciones.push({ noTerminal: ladoIzq, producciones: opciones });
  }
}

function esTerminal(sim) {
  // Terminal si no inicia con mayúscula o es epsilon
  return !/^[A-Z]/.test(sim) || sim === "ε";
}

function calcularFirst() {
  // Inicializar conjuntos FIRST vacíos
  for (const prod of producciones) {
    if (!first[prod.noTerminal]) {
      first[prod.noTerminal] = new Set();
    }
    simbolos.add(prod.noTerminal);
  }

  let cambiado;
  do {
    cambiado = false;
    for (const prod of producciones) {
      for (const regla of prod.producciones) {
        for (let i = 0; i < regla.length; i++) {
          const simbolo = regla[i];

          if (esTerminal(simbolo)) {
            if (!first[prod.noTerminal].has(simbolo)) {
              first[prod.noTerminal].add(simbolo);
              cambiado = true;
            }
            break;
          } else {
            if (!first[simbolo]) first[simbolo] = new Set();

            const antes = first[prod.noTerminal].size;
            const conjunto = new Set([...first[simbolo]]);
            conjunto.delete("ε");

            conjunto.forEach(s => first[prod.noTerminal].add(s));

            if (!first[simbolo].has("ε")) break;

            if (i === regla.length - 1) {
              first[prod.noTerminal].add("ε");
            }

            if (first[prod.noTerminal].size > antes) {
              cambiado = true;
            }
          }
        }
      }
    }
  } while (cambiado);
}

function calcularFollow() {
  for (const nt of simbolos) {
    if (!follow[nt]) follow[nt] = new Set();
  }

  if (producciones.length === 0) return;

  const inicial = producciones[0].noTerminal;
  follow[inicial].add("$");

  let cambiado;
  do {
    cambiado = false;
    for (const prod of producciones) {
      for (const regla of prod.producciones) {
        for (let i = 0; i < regla.length; i++) {
          const B = regla[i];
          if (!simbolos.has(B)) continue;

          const resto = regla.slice(i + 1);
          let firstBeta = new Set();

          if (resto.length === 0) {
            firstBeta.add("ε");
          } else {
            for (let j = 0; j < resto.length; j++) {
              const s = resto[j];
              if (esTerminal(s)) {
                firstBeta.add(s);
                break;
              } else {
                if (!first[s]) first[s] = new Set();

                const f = new Set([...first[s]]);
                f.delete("ε");
                f.forEach(x => firstBeta.add(x));

                if (!first[s].has("ε")) break;

                if (j === resto.length - 1) firstBeta.add("ε");
              }
            }
          }

          const antes = follow[B].size;
          firstBeta.forEach(s => {
            if (s !== "ε") follow[B].add(s);
          });

          if (firstBeta.has("ε")) {
            follow[prod.noTerminal].forEach(s => follow[B].add(s));
          }

          if (follow[B].size > antes) cambiado = true;
        }
      }
    }
  } while (cambiado);
}

function mostrarResultados() {
  const contenedor = document.getElementById("resultados");
  const ntOrdenados = [...simbolos].sort();

  let html = `<table class="first-follow">
    <thead>
      <tr><th>No Terminal</th><th>FIRST</th><th>FOLLOW</th></tr>
    </thead>
    <tbody>`;

  for (const nt of ntOrdenados) {
    const firstSet = first[nt] ? [...first[nt]].join(", ") : "";
    const followSet = follow[nt] ? [...follow[nt]].join(", ") : "";
    html += `<tr><td>${nt}</td><td>{ ${firstSet} }</td><td>{ ${followSet} }</td></tr>`;
  }

  html += "</tbody></table>";
  contenedor.innerHTML = html;
}

async function verificarProduccionesPasoAPaso() {
  const input = document.getElementById("grammarInput");
  const mensajeDiv = document.getElementById("mensaje");
  const highlighted = document.getElementById("highlighted");

  const lineas = input.value.split("\n");
  let salida = "";
  let todoValido = true;

  for (let i = 0; i < lineas.length; i++) {
    const linea = lineas[i].trim();

    if (linea === "") {
      salida += "\n";
      continue;
    }

    const esValida = verificarLinea(linea);
    if (esValida) {
      salida += `<div class="valid-line">${lineas[i]}</div>\n`;
    } else {
      salida += `<div class="invalid-line">${lineas[i]}</div>\n`;
      todoValido = false;
      break; // Detener en el primer error
    }

    highlighted.innerHTML = salida;
    await sleep(400);
  }

  highlighted.innerHTML = salida;

  if (todoValido) {
    // Si todo es válido, parsear gramática y calcular First y Follow
    parsearGramatica(input.value);
    calcularFirst();
    calcularFollow();
    mostrarResultados();

    mensajeDiv.textContent = "Gramática verificada correctamente.";
    mensajeDiv.className = "success";
  } else {
    mensajeDiv.textContent = "Se encontró un error de sintaxis.";
    mensajeDiv.className = "error";
    // Limpiar resultados si hay error
    document.getElementById("resultados").innerHTML = "";
  }
}

// Mantener sincronizado el scroll del textarea con el pre para el resaltado visual
const inputArea = document.getElementById("grammarInput");
const highlighted = document.getElementById("highlighted");
if (inputArea && highlighted) {
  inputArea.addEventListener("scroll", () => {
    highlighted.scrollTop = inputArea.scrollTop;
  });
}

// Evento para el botón de verificar
document.getElementById("verifyBtn").addEventListener("click", () => {
  verificarProduccionesPasoAPaso();
});
