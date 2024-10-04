var id = undefined;

function submitCoordsForm() {
    const form = document.getElementById('coordsForm');
    fetch('/generate', {
        method: 'POST',
        body: new FormData(form) 
    })
    .then(response => response.json())
    .then(data => {
        id = data['id'];
        document.getElementById('open-preview').disabled = false;
        document.getElementById('download-csv').disabled = false;
    })
    .catch(error => {
        alert("При генерации модели произошла ошибка")
        console.error('Request to /generate failed:', error);
    });
}

function generateModel() {
    document.getElementById('open-preview').disabled = true;
    document.getElementById('download-csv').disabled = true;
    document.getElementById('coordsForm').submit();
}

function openPreview() {
    window.open(`/preview?id=${id}`, 'Визуализация');
}

function downloadCSV() {
    fetch(`/download?id=${id}`, {method: 'GET'})
    .then(downloadResponse => {
        if (!downloadResponse.ok) {
            alert("При скачивании файла произошла ошибка")
            console.error('Request to /download failed:', downloadResponse.status);
        }
        return downloadResponse.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'terrain.csv');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        alert("При скачивании файла произошла ошибка")
        console.error('Request to /download failed:', error);
    });
}

function initMap() {
    var map = L.map('map').setView([55.754270, 37.619428], 8);
    var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    tiles.addTo(map);

    var top_left_marker, bottom_right_marker;
    var top_left, bottom_right;

    map.on('click', function(e) {
        if (top_left_marker == undefined) {
            top_left_marker = L.marker(e.latlng).addTo(map);
            top_left = `${e.latlng.lat},${e.latlng.lng}`;
            document.getElementById('top_left').value = top_left;
        } else if (bottom_right_marker == undefined) {
            bottom_right_marker = L.marker(e.latlng).addTo(map);
            bottom_right = `${e.latlng.lat},${e.latlng.lng}`;
            document.getElementById('bottom_right').value = bottom_right;
            document.getElementById('coordsForm').submit();
        } else {
            map.removeLayer(top_left_marker);
            map.removeLayer(bottom_right_marker);
            top_left_marker = undefined;
            bottom_right_marker = undefined;
            top_left = undefined;
            bottom_right = undefined;
            document.getElementById('top_left').value = '';
            document.getElementById('bottom_right').value = '';
        }
    });
}

function initSlider() {
    const api1 = document.getElementById('api1');
    const api2 = document.getElementById('api2');
    const slider = document.getElementById('points-slider');
    const sliderValue = document.getElementById('slider-value')

    const squaresOfNumbersUpTo100 = [];
    for (let i = 10; i <= 100; i++) {
        squaresOfNumbersUpTo100.push(i * i);
    }
    const squaresOfNumbersUpTo318 = []; // 318 ^ 2 ~= 100k
    for (let i = 10; i <= 318; i++) {
        squaresOfNumbersUpTo318.push(i * i);
    }

    let squareNumbers = squaresOfNumbersUpTo100; 

    function updateSliderMax() {
        if (api2.checked) {
            slider.max = 318 * 318;
            squareNumbers = squaresOfNumbersUpTo318;
        } else {
            slider.max = 100 * 100;
            squareNumbers = squaresOfNumbersUpTo100;
        }
        slider.value = squareNumbers.reduce((prev, curr) => {
            return Math.abs(curr - slider.value) < Math.abs(prev - slider.value) ? curr : prev;
        });
        sliderValue.textContent = slider.value;
    }

    slider.addEventListener('input', () => {
        slider.value = squareNumbers.reduce((prev, curr) => {
            return Math.abs(curr - slider.value) < Math.abs(prev - slider.value) ? curr : prev;
        });
        sliderValue.textContent = slider.value;
    });

    api1.addEventListener('change', updateSliderMax);
    api2.addEventListener('change', updateSliderMax);
    updateSliderMax();
};

function init() {
    initMap()
    initSlider()
}
