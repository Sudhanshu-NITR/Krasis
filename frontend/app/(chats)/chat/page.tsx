"use client";

import React, { useState } from 'react';
import { DocMode, Message } from '@/types/types';
import { MOCK_MODES } from '@/config/config';
import { SidebarLeft } from '@/components/chat/SidebarLeft';
import { SidebarRight } from '@/components/chat/SidebarRight';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { MessageList } from '@/components/chat/MessageList';
import { InputArea } from '@/components/chat/InputArea';

const API_URL = "http://localhost:8000/ask/stream"; 

export default function Chat() {
    const [docMode, setDocMode] = useState<DocMode>('stripe');
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);

    const activeMode = MOCK_MODES[docMode];

    const handleSendMessage = async (textOverride?: string) => {
        const query = textOverride || input;
        if (!query.trim() || isLoading) return;

        // 1. Add User Message
        const userMsg: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: query,
            timestamp: Date.now()
        };

        // 2. Add Placeholder Assistant Message
        const aiMsgId = (Date.now() + 1).toString();
        const aiMsg: Message = {
            id: aiMsgId,
            role: 'assistant',
            content: '',
            sources: [],
            timestamp: Date.now()
        };

        setMessages(prev => [...prev, userMsg, aiMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query, doc_mode: docMode })
            });

            if (!response.body) throw new Error("No response body");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let isFirstToken = true;

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                // Split by double newline as per SSE standard
                const lines = chunk.split('\n\n');

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        try {
                            const jsonStr = line.slice(6);
                            if (!jsonStr) continue;
                            
                            const data = JSON.parse(jsonStr);

                            // Handle Text Token
                            if (data.token) {
                                if (isFirstToken) {
                                    setIsLoading(false); // Stop loading spinner once text starts
                                    isFirstToken = false;
                                }

                                setMessages(prev => prev.map(msg => 
                                    msg.id === aiMsgId 
                                        ? { ...msg, content: msg.content + data.token }
                                        : msg
                                ));
                            }

                            // Handle Sources (received at end of stream)
                            if (data.sources) {
                                setMessages(prev => prev.map(msg => 
                                    msg.id === aiMsgId 
                                        ? { ...msg, sources: data.sources }
                                        : msg
                                ));
                            }
                        } catch (e) {
                            console.error("Error parsing JSON chunk", e);
                        }
                    }
                }
            }
        } catch (error) {
            console.error("Streaming error:", error);
            setMessages(prev => prev.map(msg => 
                msg.id === aiMsgId 
                    ? { ...msg, content: msg.content + "\n\n**Error:** Failed to connect to the documentation server." }
                    : msg
            ));
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-screen bg-[#09090b] text-zinc-100 font-sans overflow-hidden selection:bg-white/20">
            <SidebarLeft docMode={docMode} setDocMode={setDocMode} onModeSwitch={() => setMessages([])} />
            
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
            
            <SidebarRight activeMode={activeMode} />
        </div>
    );
}