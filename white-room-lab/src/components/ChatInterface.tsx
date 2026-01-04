'use client';

import { useState, useRef, useEffect } from 'react';
import { Message } from '@/types';
import { parseCommand, mapTargetToForm } from '@/lib/commands';

interface ChatInterfaceProps {
  onCommand?: (command: any) => void;
}

export default function ChatInterface({ onCommand }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Hallo! Ich bin der Blue Bubble. Ich kann mich in viele Formen verwandeln und dir beim Bauen helfen. Was möchtest du tun?',
      sender: 'ai',
      timestamp: Date.now(),
    }
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user',
      timestamp: Date.now(),
    };
    setMessages(prev => [...prev, userMessage]);

    // Parse command
    const parsed = parseCommand(input);
    console.log('Parsed command:', parsed);

    // Generate AI response
    let aiResponse = '';
    
    if (parsed.intent === 'transform') {
      const form = mapTargetToForm(parsed.target || '');
      if (form) {
        aiResponse = `Okay! Ich verwandle mich jetzt in ${form}. Das dauert einen Moment...`;
        if (onCommand) {
          onCommand({ type: 'transform', form });
        }
      } else {
        aiResponse = `Ich verstehe nicht genau, in was ich mich verwandeln soll. Kannst du es anders formulieren?`;
      }
    } else if (parsed.intent === 'create') {
      aiResponse = `Ich möchte ${parsed.target} bauen. Dafür brauche ich ein CAD-Werkzeug. Darf ich es installieren?`;
      if (onCommand) {
        onCommand({ type: 'permission_request', action: 'install_cad_tool', target: parsed.target });
      }
    } else if (parsed.intent === 'help') {
      aiResponse = `Hier sind meine Fähigkeiten:\n- Verwandlungen (DNA, Neural Network, Molecule, City, Galaxy)\n- Bauen und Erstellen\n- Simulationen\n\nSag mir einfach, was du möchtest!`;
    } else {
      aiResponse = `Ich habe verstanden: "${parsed.target}". Was möchtest du damit machen?`;
    }

    // Add AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiResponse,
        sender: 'ai',
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, aiMessage]);
    }, 500);

    setInput('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex-1 max-w-md bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-4 flex flex-col">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto mb-4 space-y-3 max-h-64">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              <p className="text-sm">{message.content}</p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Schreibe einen Befehl..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
        <button
          onClick={handleSend}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm font-medium"
        >
          Senden
        </button>
      </div>
    </div>
  );
}
