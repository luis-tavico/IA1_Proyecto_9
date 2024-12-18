let model, words, classes, intents;

async function loadResources() {
    model = await tf.loadLayersModel('./modelo/model_js/model.json');
    const wordsResponse = await fetch('./modelo/words.json');
    words = await wordsResponse.json();

    const classesResponse = await fetch('./modelo/classes.json');
    classes = await classesResponse.json();

    const intentsResponse = await fetch('./modelo/intents_combinate.json');
    intents = await intentsResponse.json();
}

function bagOfWords(sentence) {
    const sentenceWords = sentence.toLowerCase().split(' ');
    const bag = new Array(words.length).fill(0);

    sentenceWords.forEach(word => {
        const index = words.indexOf(word);
        if (index !== -1) {
            bag[index] = 1;
        }
    });
    return tf.tensor2d([bag]);
}

async function predictClass(sentence) {
    const bow = bagOfWords(sentence);
    const predictions = await model.predict(bow).data();
    const maxIndex = predictions.indexOf(Math.max(...predictions));
    return classes[maxIndex];
}

function getResponse(tag) {
    const intent = intents.intents.find(intent => intent.tag === tag);
    if (intent) {
        const responses = intent.responses;
        return responses[Math.floor(Math.random() * responses.length)];
    }
    return "No entiendo tu mensaje, intenta de nuevo.";
}

async function respuesta(message) {
    const tag = await predictClass(message);
    return getResponse(tag);
}

function mostrarMensaje(mensaje, clase) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', clase);
    messageElement.innerHTML = `<p>${mensaje}</p>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function enviarMensaje() {
    const input = document.getElementById('chat-input');
    const mensajeUsuario = input.value.trim();
    if (!mensajeUsuario) return;

    mostrarMensaje(mensajeUsuario, 'user');
    const respuestaBot = await respuesta(mensajeUsuario);
    mostrarMensaje(respuestaBot, 'bot');
    input.value = '';
}

document.getElementById('send-button').addEventListener('click', enviarMensaje);
document.getElementById('chat-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        enviarMensaje();
    }
});

loadResources();