const apiUrl = '/api/orders'; // Esta es la URL de tu API Flask

let rawData = []; // Almacenará los datos brutos de la API
let myDataTable; // Variable para la instancia de DataTables
let charts = []; // Almacenará las instancias de Chart.js

$(document).ready(function () {
    // 1. Cargar los datos al inicio
    loadOrders();

    // 2. Event listeners para los filtros
    $('#categoryFilter, #regionFilter, #segmentFilter').on('change', function () {
        const filteredData = filterData();
        updateTable(filteredData);
        updateCharts(filteredData);
    });
});

/**
 * Carga los datos de órdenes desde la API de Flask.
 */
function loadOrders() {
    $.ajax({
        url: apiUrl,
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            rawData = data;
            console.log("Datos cargados de la API:", rawData);
            populateFilters();
            initializeTable(rawData); // Inicializa la tabla DataTables
            drawAllCharts(rawData);
        },
        error: function (xhr, status, error) {
            console.error('Error fetching data:', status, error);
            alert('No se pudieron cargar los datos. Asegúrate de que el backend esté funcionando.');
        }
    });
}

/**
 * Rellena los selectores de filtro con opciones únicas de los datos.
 */
function populateFilters() {
    populateSelect('Category', '#categoryFilter');
    populateSelect('Region', '#regionFilter');
    populateSelect('Segment', '#segmentFilter');
}

/**
 * Helper para rellenar un selector HTML.
 * @param {string} key La clave del objeto de datos para extraer las opciones.
 * @param {string} selector El selector jQuery del elemento <select>.
 */
function populateSelect(key, selector) {
    const options = [...new Set(rawData.map(item => item[key]))].sort(); // Obtiene únicos y los ordena
    $(selector).empty().append(`<option value="">Todos</option>`); // Añade opción "Todos"
    options.forEach(opt => {
        if (opt !== null && opt !== undefined && opt !== '') { // Evita opciones nulas/vacías
            $(selector).append(`<option value="${opt}">${opt}</option>`);
        }
    });
}

/**
 * Filtra los datos brutos basándose en los valores seleccionados en los filtros.
 * @returns {Array} Los datos filtrados.
 */
function filterData() {
    const category = $('#categoryFilter').val();
    const region = $('#regionFilter').val();
    const segment = $('#segmentFilter').val();

    return rawData.filter(item =>
        (category === '' || item['Category'] === category) &&
        (region === '' || item['Region'] === region) &&
        (segment === '' || item['Segment'] === segment)
    );
}

/**
 * Inicializa la tabla DataTables con los datos proporcionados.
 * @param {Array} data Los datos para mostrar en la tabla.
 */
function initializeTable(data) {
    // Si la tabla ya está inicializada, la destruimos primero
    if ($.fn.DataTable.isDataTable('#dataTable')) {
        $('#dataTable').DataTable().destroy();
    }

    // Mapea las columnas para DataTables
    const columns = Object.keys(data[0] || {}).map(key => {
        let title = key.replace(/([A-Z])/g, ' $1').trim(); // Añade espacio antes de mayúsculas
        return { title: title, data: key };
    });

    myDataTable = $('#dataTable').DataTable({
        data: data,
        columns: columns,
        destroy: true, // Permite reinicializar la tabla
        pageLength: 10,
        responsive: true // Hace la tabla responsiva
    });
}

/**
 * Actualiza los datos de la tabla DataTables existente.
 * @param {Array} data Los datos actualizados.
 */
function updateTable(data) {
    if (myDataTable) {
        myDataTable.clear().rows.add(data).draw();
    } else {
        initializeTable(data); // Si por alguna razón no se inicializó, lo hacemos
    }
}

/**
 * Destruye todas las instancias de Chart.js existentes.
 */
function destroyCharts() {
    charts.forEach(chart => chart.destroy());
    charts = [];
}

/**
 * Dibuja todos los gráficos con los datos proporcionados.
 * @param {Array} data Los datos para los gráficos.
 */
function drawAllCharts(data) {
    destroyCharts(); // Limpia gráficos anteriores

    // Asegúrate de que las fechas estén en formato Date para Chart.js si se usan en ejes de tiempo
    const processedData = data.map(item => ({
        ...item,
        OrderDate: item.OrderDate ? new Date(item.OrderDate) : null,
        ShipDate: item.ShipDate ? new Date(item.ShipDate) : null
    }));

    charts.push(drawChart('chartBar', 'bar', groupSum(processedData, 'Category', 'Sales'), 'Ventas por Categoría'));
    charts.push(drawChart('chartPie', 'pie', groupSum(processedData, 'Region', 'Profit'), 'Ganancias por Región'));
    charts.push(drawChart('chartLine', 'line', groupSum(processedData, 'OrderDate', 'Sales', true), 'Ventas a lo largo del Tiempo'));
    charts.push(drawChart('chartRadar', 'radar', groupSum(processedData, 'Segment', 'Quantity'), 'Cantidad por Segmento'));

    charts.push(drawChart('chart1', 'bar', groupSum(processedData, 'SubCategory', 'Sales'), 'Ventas por Sub-Categoría'));
    charts.push(drawChart('chart2', 'doughnut', groupSum(processedData, 'ShipMode', 'Sales'), 'Ventas por Modo de Envío'));
    charts.push(drawChart('chart3', 'bar', groupSum(processedData, 'Region', 'Quantity'), 'Cantidad por Región'));
    charts.push(drawChart('chart4', 'line', groupSum(processedData, 'ShipDate', 'Profit', true), 'Ganancias a lo largo del Tiempo (Envío)'));
    charts.push(drawChart('chart5', 'pie', groupSum(processedData, 'Segment', 'Sales'), 'Ventas por Segmento'));
    charts.push(drawChart('chart6', 'bar', groupSum(processedData, 'Category', 'Profit'), 'Ganancias por Categoría'));
}

/**
 * Actualiza los gráficos con nuevos datos.
 * @param {Array} data Los datos actualizados.
 */
function updateCharts(data) {
    drawAllCharts(data); // Simplemente redibujamos todos los gráficos para simplicidad con filtros
}

/**
 * Dibuja un gráfico Chart.js.
 * @param {string} canvasId El ID del elemento canvas HTML.
 * @param {string} type El tipo de gráfico (bar, pie, line, etc.).
 * @param {object} chartData Los datos formateados para el gráfico.
 * @param {string} title El título del gráfico.
 * @returns {Chart} La instancia de Chart.js.
 */
function drawChart(canvasId, type, chartData, title) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) {
        console.warn(`Canvas con ID ${canvasId} no encontrado.`);
        return;
    }
    return new Chart(ctx.getContext('2d'), {
        type: type,
        data: {
            labels: chartData.labels,
            datasets: [{
                label: title,
                data: chartData.values,
                backgroundColor: generateColors(chartData.labels.length, 0.7),
                borderColor: generateColors(chartData.labels.length, 1),
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Permite que los gráficos se ajusten a su contenedor
            plugins: {
                title: {
                    display: true,
                    text: title,
                    font: { size: 16, weight: 'bold' },
                    color: '#343a40'
                },
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#343a40'
                    }
                },
                tooltip: {
                    backgroundColor: '#fff',
                    titleColor: '#343a40',
                    bodyColor: '#343a40',
                    borderColor: '#ddd',
                    borderWidth: 1
                }
            },
            scales: type === 'radar' || type === 'pie' || type === 'doughnut' ? {} : {
                x: {
                    ticks: { color: '#666' },
                    grid: { color: '#eee' },
                    type: chartData.isTime ? 'time' : 'category', // Usa 'time' si se procesó como fecha
                    time: {
                        unit: 'year' // Ajustar la unidad según la granularidad de tus fechas
                    }
                },
                y: {
                    ticks: { color: '#666' },
                    grid: { color: '#eee' },
                    beginAtZero: true
                }
            }
        }
    });
}

/**
 * Agrupa y suma valores de datos.
 * @param {Array} data Los datos brutos.
 * @param {string} key La clave para agrupar (e.g., 'Category').
 * @param {string} valueKey La clave para sumar (e.g., 'Sales').
 * @param {boolean} parseDate Si la clave de agrupación es una fecha y debe parsearse.
 * @returns {object} Un objeto con labels (etiquetas), values (valores sumados) y label (título).
 */
function groupSum(data, key, valueKey, parseDate = false) {
    const grouped = {};

    data.forEach(item => {
        let groupKey = item[key];
        if (parseDate && item[key]) {
            // Para ejes de tiempo, usa el objeto Date directamente para que Chart.js lo maneje
            groupKey = item[key]; // Ya está como objeto Date por el pre-procesamiento
        } else if (item[key] === null || item[key] === undefined) {
             groupKey = 'Desconocido'; // Manejar valores nulos para la clave
        }

        if (!grouped[groupKey]) grouped[groupKey] = 0;
        grouped[groupKey] += parseFloat(item[valueKey]) || 0;
    });

    let labels = Object.keys(grouped);
    let values = labels.map(k => grouped[k]);

    // Si es un eje de tiempo, asegurar el orden cronológico
    if (parseDate) {
        // Ordenar etiquetas de fecha si son objetos Date
        labels.sort((a, b) => a - b);
        values = labels.map(k => grouped[k]);
    } else {
        // Para categorías, ordenar alfabéticamente
        labels.sort();
        values = labels.map(k => grouped[k]);
    }


    return { labels, values, label: `${valueKey} por ${key}`, isTime: parseDate };
}

/**
 * Genera una paleta de colores aleatoria o predefinida.
 * @param {number} numColors La cantidad de colores a generar.
 * @param {number} opacity La opacidad de los colores.
 * @returns {Array<string>} Un array de cadenas de color.
 */
function generateColors(numColors, opacity = 1) {
    const colorPalette = [
        'rgba(255, 99, 132, OPACITY)', // Red
        'rgba(54, 162, 235, OPACITY)', // Blue
        'rgba(255, 206, 86, OPACITY)', // Yellow
        'rgba(75, 192, 192, OPACITY)', // Green
        'rgba(153, 102, 255, OPACITY)', // Purple
        'rgba(255, 159, 64, OPACITY)', // Orange
        'rgba(199, 199, 199, OPACITY)', // Grey
        'rgba(255, 102, 0, OPACITY)',  // Dark Orange
        'rgba(0, 153, 153, OPACITY)',  // Teal
        'rgba(204, 0, 204, OPACITY)'   // Magenta
    ];
    let colors = [];
    for (let i = 0; i < numColors; i++) {
        colors.push(colorPalette[i % colorPalette.length].replace(/OPACITY/g, opacity));
    }
    return colors;
}