import './App.css';

function App() {
  return (
    <div className="chat-container">
      <div className="conversation-area">
        <header className="text-center p-3 bg-primary text-white">
          <h2>Chatbot</h2>
        </header>
        <main className="messages-area" id="chat-log">
          <div className="message sent">
            <div className="message-content">
              <p><strong>Tu: </strong>Hola, ¿Quién eres?</p>
              <span className="time">06:20 p.m.</span>
            </div>
          </div>
          <div className="message received">
            <img src="/images/bot.png" alt="Chatbot" className="message-image" />
          <div className="message-content">
              <p><strong>Chatbot: </strong>Soy un chatbot simple.</p>
              <span className="time">06:20 p.m.</span>
            </div>
          </div>
        </main>
        <footer className="message-input p-3 border-top">
          <textarea id="user-input" rows="2" placeholder="Escribe un mensaje" className="form-control me-2"></textarea>
          <button id="send-button" className="btn btn-primary" onClick={sendMessage}>Enviar</button>
        </footer>
      </div>
    </div>
  );
}

function sendMessage() {
  console.log("Message sent!");
}

export default App;