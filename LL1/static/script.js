function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function verificarLinea(linea) {
  const regexProduccion = /^([A-Z][0-9']*)\s*(→|->|=)\s*(.+)$/;
  const regexCuerpo = /^([^|]+)(\s*\|\s*[^|]+)*$/;

  const match = regexProduccion.exec(linea);
  if (!match) return false;

  const cuerpo = match[3].trim();
  return regexCuerpo.test(cuerpo);
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

  mensajeDiv.textContent = todoValido
    ? "Gramática verificada correctamente."
    : "Se encontró un error de sintaxis.";
  mensajeDiv.className = todoValido ? "success" : "error";
}

document.getElementById("verifyBtn").addEventListener("click", () => {
  verificarProduccionesPasoAPaso();
});
