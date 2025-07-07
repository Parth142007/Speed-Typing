var startTime = null;
var timerDuration = parseInt(document.getElementById("timer").textContent);
var timerElement = document.getElementById("timer");
var userInput = document.getElementById("userInput");
var wpmElement = document.getElementById("wpm");
var accuracyElement = document.getElementById("accuracy");
var elapsedElement = document.getElementById("elapsed");
var paragraphElement = document.getElementById("paragraph");
var resultsElement = document.getElementById("results");
var realtimeUpdateElement = document.getElementById("realtime_update");
var elapsedTime = 0;


function resetTimer() {
    clearInterval(timerInterval);
    startTime = null;
    elapsedTime = 0;
    elapsedElement.innerText = '0';
    timerElement.innerText = timerDuration;
    userInput.disabled = false;
    $('input[type="submit"]').removeAttr('disabled');
    resultsElement.style.display = 'none';
}


function updateTimer() {
    if (startTime !== null) {
        var timeRemaining = timerDuration - Math.floor((Date.now() - startTime) / 1000);
        timerElement.innerText = timeRemaining;

        if (timeRemaining <= 0) {
            userInput.disabled = true;
            $('input[type="submit"]').attr('disabled', 'disabled');
            resetTimer();
        }
    }
}


function updateResults() {
    if (startTime !== null) {
        $.ajax({
            type: 'POST',
            url: '/typing-result',
            data: $('#typingForm').serialize(),
            success: function (data) {
                wpmElement.innerText = data.words_per_minute.toFixed(2);
                accuracyElement.innerText = data.accuracy.toFixed(2);
                elapsedTime = data.time_elapsed;
                elapsedElement.innerText = elapsedTime.toFixed(2);

                resultsElement.innerHTML = `
                    <h4>Words per Minute: ${data.words_per_minute.toFixed(2)}</h4>
                    <h4>Accuracy: ${data.accuracy.toFixed(2)}%</h4>
                    <h4>Time Elapsed: ${elapsedTime.toFixed(2)} seconds</h4>
                    <h4>Number of Words: ${data.word_count} words</h4>
                `;
            },
            dataType: 'json'
        });
    }
}


userInput.addEventListener('input', function () {
    if (startTime === null) {
        startTime = Date.now();
        timerInterval = setInterval(function () {
            updateTimer();
            updateResults();
        }, 1000);
        resultsElement.style.display = 'none';
    }
});


var modal = document.getElementById("resultsModal");
var closeBtn = document.getElementsByClassName("close")[0];


function openModal(data) {
    document.getElementById("modal-wpm").innerText = data.words_per_minute.toFixed(2);
    document.getElementById("modal-accuracy").innerText = data.accuracy.toFixed(2) + "%";
    document.getElementById("modal-elapsed").innerText = data.time_elapsed.toFixed(2) + "s";
    document.getElementById("modal-word-count").innerText = data.word_count;
    modal.style.display = "block";
}


closeBtn.onclick = function () {
    modal.style.display = "none";
    location.reload();
};


window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};


$('#typingForm').on('submit', function (e) {
    e.preventDefault();
    resetTimer();
    updateTimer();
    updateResults();

    $.ajax({
        type: 'POST',
        url: '/typing-result',
        data: $('#typingForm').serialize(),
        success: function (data) {
            openModal(data);
        },
        dataType: 'json'
    });
    userInput.value = '';
});


$('#changeParagraphButton').click(function () {
    $.ajax({
        type: 'POST',
        url: '/change_paragraph',
        success: function (data) {
            paragraphElement.innerText = data;
            resetTimer();
            updateTimer();
            updateResults();
            resultsElement.style.display = 'none';
            userInput.value = '';
            userInput.disabled = false;
            $('input[type="submit"]').removeAttr('disabled');
        },
        dataType: 'text'
    });
});


$(document).ready(function () {
    resetTimer();
    updateTimer();
    updateResults();
});