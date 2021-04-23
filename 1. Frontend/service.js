// AWS API Gateway endpoint
var API_ENDPOINT = 'https://pqg0t3hlk0.execute-api.us-east-1.amazonaws.com/prod/petcuddleotron';

var errorDiv = document.getElementById('error-message')
var successDiv = document.getElementById('success-message')
var resultsDiv = document.getElementById('results-message')

// function output returns input button contents
function messageValue() { return document.getElementById('message').value }
function emailValue() { return document.getElementById('email').value }
function phoneValue() { return document.getElementById('phone').value }
function buysellValue() { return document.querySelector('input[name="buysell"]:checked').value }
function priceValue() { return document.querySelector('input[name="price"]:checked').value }
function carValue() { return document.querySelector('input[name="car"]:checked').value }

function clearNotifications() {
    errorDiv.textContent = '';
    resultsDiv.textContent = '';
    successDiv.textContent = '';
}

// When buttons are clicked, these are run passing values to API Gateway call
document.getElementById('submitButton').addEventListener('click', function(e) { sendData(e); });


function sendData (e) {
    e.preventDefault()
    clearNotifications()
    fetch(API_ENDPOINT, {
        headers:{
            "Content-type": "application/json"
        },
        method: 'POST',
        body: JSON.stringify({
            message: messageValue(),
            email: emailValue(),
            phone: phoneValue(),
			buysell: buysellValue(),
			price: priceValue(),
			car: carValue()
        }),
        mode: 'cors'
    })
    .then((resp) => resp.json())
    .then(function(data) {
        console.log(data)
        successDiv.textContent = 'Submitted';
        resultsDiv.textContent = JSON.stringify(data);
    })
    .catch(function(err) {
        errorDiv.textContent = 'Error:\n' + err.toString();
        console.log(err)
    });
};
