// Get references to HTML elements
const messagesContainer = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Array to store chat history
const chatHistory = [];

// Event listener for send button click
sendButton.addEventListener('click', sendMessage);

// Event listener for user pressing Enter key
userInput.addEventListener('keyup', function(event) {
  if (event.keyCode === 13) {
    sendMessage();
  }
});

// Function to send a message
function sendMessage() {
  const message = userInput.value;
  displayMessage(message, 'user');
  chatHistory.push({ message, sender: 'user' });
  callLambdaFunction(message);
  userInput.value = '';
}

// Function to display a message in the chat interface
function displayMessage(message, sender) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', sender);
  messageElement.innerText = message;
  messagesContainer.appendChild(messageElement);
}

// Function to call the AWS Lambda function
function callLambdaFunction(message) {
  // Make an AJAX request to your AWS Lambda function
  // Here's an example using the Fetch API
  fetch('https://uuy3smgrol62kzfd26sxicfaxu0vezci.lambda-url.us-west-2.on.aws/', {
    method: 'POST',
    body: JSON.stringify({ message }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    const botResponse = data.response;
    displayMessage(botResponse, 'bot');
    chatHistory.push({ message: botResponse, sender: 'bot' });
  })
  .catch(error => {
    console.error('Error:', error);
  });
}