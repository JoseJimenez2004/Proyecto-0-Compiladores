// Función para manejar la carga del archivo
document.getElementById('verAutomataBtn').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

// Función para leer el archivo y procesar el texto
document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file && file.name.endsWith('.txt')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const fileContent = e.target.result;
            console.log("Contenido del archivo:", fileContent);  // Ver contenido del archivo
            const automataData = parseAutomata(fileContent);
            console.log("Datos del autómata:", automataData);  // Ver datos del autómata
            openNewTabAndDrawGraph(automataData);
        };
        reader.readAsText(file);
    } else {
        alert('Por favor, selecciona un archivo .txt');
    }
});

// Función para parsear el contenido del archivo .txt
function parseAutomata(fileContent) {
    const automata = {
        simbolo: '',
        estadoInicial: '',
        estadoFinal: '',
        transiciones: []
    };
    const lines = fileContent.split('\n');
    lines.forEach(line => {
        if (line.startsWith('AFN con símbolo')) {
            automata.simbolo = line.split(': ')[1];
        } else if (line.startsWith('Estado inicial')) {
            automata.estadoInicial = parseInt(line.split(': ')[1]);
        } else if (line.startsWith('Estado final')) {
            automata.estadoFinal = parseInt(line.split(': ')[1]);
        } else if (line.startsWith('Transiciones')) {
            const transiciones = line.split(': ')[1].slice(1, -1).split(', ');
            transiciones.forEach(transition => {
                const [from, symbol, to] = transition.replace(/[()']/g, '').split(', ');
                automata.transiciones.push({ from: parseInt(from), symbol, to: parseInt(to) });
            });
        }
    });
    return automata;
}

// Función para abrir una nueva pestaña y dibujar el grafo allí
function openNewTabAndDrawGraph(automataData) {
    // Abrir una nueva pestaña
    const newTab = window.open('', '_blank');  // Abrimos la nueva pestaña

    // Escribir HTML básico en la nueva pestaña
    newTab.document.write('<html><head><title>Grafo del Automáta</title></head><body>');
    newTab.document.write('<h2>Visualización del Grafo del Automáta</h2>');
    newTab.document.write('<div id="network" style="width: 100%; height: 500px; border: 2px solid #ddd; padding: 10px;"></div>');
    newTab.document.write('<script type="text/javascript" src="https://unpkg.com/vis@4.21.0/dist/vis-network.min.js"></script>');
    newTab.document.write('<script type="text/javascript">');
    newTab.document.write(`
        const automataData = ${JSON.stringify(automataData)};
        
        // Definición de nodos
        var nodes = new vis.DataSet([
            ${Array.from(new Set(automataData.transiciones.flatMap(t => [t.from, t.to]))).map(node => {
                // Si el nodo es el estado final, le asignamos doble círculo
                const isFinalState = automataData.estadoFinal === node;
                return `{ id: ${node}, label: '${node}', shape: 'circle', font: { multi: 'html' }, ${
                    isFinalState ? 'size: 30, borderWidth: 6, borderWidthSelected: 6' : ''
                } }`;
            }).join(',\n')}
        ]);

        // Definición de aristas (enlaces)
        var edges = new vis.DataSet([
            ${automataData.transiciones.map(t => `{ from: ${t.from}, to: ${t.to}, label: '${t.symbol}', arrows: 'to' }`).join(',\n')}
        ]);

        // Obtener el contenedor donde se visualizará el grafo
        var container = document.getElementById('network');
        var data = { nodes: nodes, edges: edges };

        // Configuración para visualización
        var options = {
            layout: {
                randomSeed: 2,  // Esto ayuda a generar una distribución más controlada
                improvedLayout: true,  // Mejor distribución automática
                hierarchical: {
                    direction: 'LR'  // Disposición jerárquica de izquierda a derecha
                }
            },
            physics: {
                enabled: false  // Deshabilitar la física para evitar que los nodos se muevan
            },
            manipulation: {
                enabled: false  // Deshabilita la manipulación directa de los nodos
            }
        };

        // Crear el grafo en el contenedor
        var network = new vis.Network(container, data, options);
    `);
    newTab.document.write('</script>');
    newTab.document.write('</body></html>');
}
