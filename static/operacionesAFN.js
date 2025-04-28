document.addEventListener('DOMContentLoaded', function() {
    // Función para realizar una solicitud POST al backend
    function postRequest(url, data, callback) {
        fetch(url, {
            method: 'POST',
            body: data,  // Enviar los datos como FormData o JSON según corresponda
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                callback(data);
            }
        })
        .catch(error => {
            alert('Error: ' + error);
        });
    }

    // Unir AFNs
    const formUnirAFNs = document.getElementById('form-unir-afns');
    if (formUnirAFNs) {
        formUnirAFNs.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar recarga de página

            const afn1Input = document.getElementById('afn1');
            const afn2Input = document.getElementById('afn2');
            const nombreInput = document.getElementById('nombre');

            // Verificar que los archivos y el nombre no estén vacíos
            if (!afn1Input.files.length || !afn2Input.files.length || !nombreInput.value) {
                alert('Por favor, completa todos los campos.');
                return;
            }

            const afn1File = afn1Input.files[0];
            const afn2File = afn2Input.files[0];

            // Crear un objeto FormData para enviar los archivos al backend
            const formData = new FormData();
            formData.append('afn1', afn1File);
            formData.append('afn2', afn2File);
            formData.append('nombre', nombreInput.value);  // Asegúrate de que el nombre esté incluido también

            // Enviar la solicitud POST con los archivos y el nombre del archivo de resultado
            postRequest('/unir_afns', formData, function(response) {
                alert('AFNs unidos exitosamente!');
                console.log(response);
            });
        });
    }

    // Concatenar AFNs
    const concatenarButton = document.getElementById('concatenarButton');
    if (concatenarButton) {
        concatenarButton.addEventListener('click', function() {
            const data = {}; // Puedes agregar los datos necesarios aquí si es necesario
            postRequest('/concatenar_afn', data, function(response) {
                alert('AFN concatenado exitosamente!');
                console.log(response);
            });
        });
    }

    // Cerradura positiva
    const cerraduraPositivaButton = document.getElementById('cerraduraPositivaButton');
    if (cerraduraPositivaButton) {
        cerraduraPositivaButton.addEventListener('click', function() {
            const data = {}; // Puedes agregar los datos necesarios aquí si es necesario
            postRequest('/cerradura_positiva', data, function(response) {
                alert('Cerradura positiva aplicada exitosamente!');
                console.log(response);
            });
        });
    }

    // Cerradura de Kleene
    const cerraduraKleeneButton = document.getElementById('cerraduraKleeneButton');
    if (cerraduraKleeneButton) {
        cerraduraKleeneButton.addEventListener('click', function() {
            const nombreAFN = document.getElementById('nombreCerraduraKleene').value;

            if (!nombreAFN) {
                alert("Por favor, ingresa el nombre del AFN.");
                return;
            }

            const data = { nombre: nombreAFN };

            postRequest('/cerradura_kleene', data, function(response) {
                alert(response.mensaje || 'Cerradura de Kleene aplicada exitosamente!');
                console.log(response);
            });
        });
    }

    // Cerradura opcional
    const cerraduraOpcionalButton = document.getElementById('cerraduraOpcionalButton');
    if (cerraduraOpcionalButton) {
        cerraduraOpcionalButton.addEventListener('click', function() {
            const data = {}; // Puedes agregar los datos necesarios aquí si es necesario
            postRequest('/cerradura_opcional', data, function(response) {
                alert('Cerradura opcional aplicada exitosamente!');
                console.log(response);
            });
        });
    }

    // Analizador léxico
    const analizadorButton = document.getElementById('analizadorButton');
    if (analizadorButton) {
        analizadorButton.addEventListener('click', function() {
            const cadena = document.getElementById('cadena').value;

            if (!cadena) {
                alert("Por favor, ingresa una cadena.");
                return;
            }

            const data = { cadena: cadena };

            postRequest('/analizador_lexico', data, function(response) {
                const tokensDiv = document.getElementById('tokens');
                tokensDiv.innerHTML = ''; // Limpiar los tokens anteriores

                if (response.tokens) {
                    response.tokens.forEach(function(token) {
                        const tokenElement = document.createElement('div');
                        tokenElement.textContent = `Lexema: ${token.lexema}, Token: ${token.token}`;
                        tokensDiv.appendChild(tokenElement);
                    });
                }
            });
        });
    }
});
