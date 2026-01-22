"use client";

import React, { useState } from 'react';
import { DocMode, Message } from '@/types/types';
import { MOCK_MODES } from '@/config/config';
import { SidebarLeft } from '@/components/chat/SidebarLeft';
import { SidebarRight } from '@/components/chat/SidebarRight';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { MessageList } from '@/components/chat/MessageList';
import { InputArea } from '@/components/chat/InputArea';

const USE_MOCK_API = true;
const API_URL = "http://localhost:8000/ask";

export default function Chat() {
    const [docMode, setDocMode] = useState<DocMode>('stripe');
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);

    const activeMode = MOCK_MODES[docMode];

    const handleSendMessage = async (textOverride?: string) => {
        const query = textOverride || input;
        if (!query.trim() || isLoading) return;

        const userMsg: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: query,
            timestamp: Date.now()
        };

        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            let responseData;
            if (USE_MOCK_API) {
                await new Promise(resolve => setTimeout(resolve, 2000));
                const mockContent = `Here is how you handle this in **${activeMode.name}**.\n\nFirst, initialize the client with your secret key.\n\n\`\`\`javascript\nconst client = new Client({\n  apiKey: process.env.API_KEY,\n  version: '${activeMode.context.version}'\n});\n\nconst result = await client.post('${activeMode.context.popularEndpoints[0]}', {\n  metadata: { source: 'devdocs-ai' }\n});\n\`\`\`\n\nThe API returns a JSON object. Ensure you handle rate limits correctly.`;

                responseData = {
                    answer: mockContent,
                    sources: [{ title: `${activeMode.name} Reference`, url: '#' }, { title: 'Rate Limiting Guide', url: '#' }]
                };
            } else {
                const res = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, doc_mode: docMode })
                });
                if (!res.ok) throw new Error('API Error');
                responseData = await res.json();
            }

            const aiMsg: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: responseData.answer || responseData.content,
                sources: responseData.sources || [],
                timestamp: Date.now()
            };

            setMessages(prev => [...prev, aiMsg]);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-[#09090b] text-zinc-100 font-sans overflow-hidden selection:bg-white/20">

            {/* Sidebar Left */}
            <SidebarLeft docMode={docMode} setDocMode={setDocMode} onModeSwitch={() => setMessages([])} />

            {/* Main Chat Area */}
            <main className="flex-1 flex flex-col relative min-w-0">
                <ChatHeader activeMode={activeMode} />

                <MessageList
                    messages={messages}
                    isLoading={isLoading}
                    activeMode={activeMode}
                    onSuggestionClick={handleSendMessage}
                />

                <InputArea
                    input={input}
                    setInput={setInput}
                    onSend={() => handleSendMessage()}
                    isLoading={isLoading}
                    docMode={docMode}
                />
            </main>

            {/* Sidebar Right */}
            <SidebarRight activeMode={activeMode} />

        </div>
    );
}