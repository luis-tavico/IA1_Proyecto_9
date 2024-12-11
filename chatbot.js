let ChatbotConfig = {};

// Función para cargar la configuración desde un archivo JSON
async function loadChatbotConfig() {
    try {
        const response = await fetch('./modelo/intents.json'); // Ruta del archivo JSON
        const data = await response.json();
        ChatbotConfig = data;
        console.log('ChatbotConfig loaded:', ChatbotConfig);
    } catch (error) {
        console.error('Error loading chatbot configuration:', error);
    }
}

async function loadModel() {
    try {
        const modelUrl = './modelo/model.onnx'; // Asegúrate de que el archivo esté en la ruta correcta
        const session = await ort.InferenceSession.create(modelUrl);
        console.log('Model loaded');
        return session;
    } catch (error) {
        console.error('Error loading model:', error);
    }
}

async function runInference(session, inputData) {
    try {
        const inputTensor = new ort.Tensor('float32', inputData, [1, inputData.length]);
        const feeds = { input: inputTensor };

        const results = await session.run(feeds);

        const outputName = session.outputNames[0];
        const resultData = results[outputName].data;

        return resultData;
    } catch (error) {
        console.error('Error running inference:', error);
        return null; // Manejar errores sin detener la ejecución
    }
}

async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    document.getElementById('user-input').value=""; // Limpiar el input
    // Preprocesar entrada
    const inputData = preprocessInput(userInput);

    const model = await loadModel();
    if (model) {
        const outputData = await runInference(model, inputData);

        // Obtener la respuesta del chatbot
        const response = outputData ? getChatbotResponse(outputData) : "Hubo un problema con el modelo.";
        displayMessage('YO:', userInput);
        displayMessage('Chatbot', response);
    }
}

function preprocessInput(userInput) {
    const tokens = userInput.toLowerCase().split(" ");
    const allWords = ChatbotConfig.intents.flatMap(intent => intent.patterns);
    //console.log('All words:', allWords);
    const uniqueWords = Array.from(new Set(allWords));
    
    // Crear "bag of words"
    let bag = uniqueWords.map(word => (tokens.includes(word) ? 1 : 0));
    
    // Ajustar el tamaño del array al tamaño esperado por el modelo
    const expectedSize = 483;
    if (bag.length > expectedSize) {
        bag = bag.slice(0, expectedSize); // Truncar si es mayor
    } else if (bag.length < expectedSize) {
        bag = bag.concat(new Array(expectedSize - bag.length).fill(0)); // Rellenar con ceros si es menor
    }
    
    return new Float32Array(bag);
}

function getChatbotResponse(responseVector) {
    if (!responseVector || responseVector.length === 0) {
        return "Lo siento, no puedo procesar tu solicitud en este momento.";
    }

    // Encontrar el índice con el valor más alto en el vector
    const maxIndex = responseVector.indexOf(Math.max(...responseVector));
    const tag = ChatbotConfig.intents[maxIndex]?.tag;

    // Obtener las respuestas asociadas al tag
    const intent = ChatbotConfig.intents.find(i => i.tag === tag);
    const responses = intent?.responses || ["Lo siento, no entendí eso."];

    // Seleccionar una respuesta aleatoria
    return responses[Math.floor(Math.random() * responses.length)];
}

function displayMessage(sender, message) {
    const chatWindow = document.getElementById('chat-log');
    const messageDiv = document.createElement('div');
    messageDiv.textContent = `${sender}: ${message}`;
    chatWindow.appendChild(messageDiv);
}

// Cargar la configuración del chatbot al inicio
loadChatbotConfig();