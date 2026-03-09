"use client";

import React, { useState } from 'react';
import { DocMode, Message } from '@/types/types';
import { MOCK_MODES } from '@/config/config';
import { SidebarLeft } from '@/components/chat/SidebarLeft';
import { SidebarRight } from '@/components/chat/SidebarRight';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { MessageList } from '@/components/chat/MessageList';
import { InputArea } from '@/components/chat/InputArea';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || '';

export default function Chat() {
    const [docMode, setDocMode] = useState<DocMode>('langchain');
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);

    // Sidebar States
    const [isLeftOpen, setIsLeftOpen] = useState(true);
    const [isRightOpen, setIsRightOpen] = useState(true);

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

        const historyPayload = messages.map(msg => ({
            role: msg.role,
            content: msg.content
        }));

        setMessages(prev => [...prev, userMsg, aiMsg]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch(`${API_URL}/ask/stream`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    doc_mode: docMode,
                    chat_history: historyPayload
                })
            });

            if (!response.body) throw new Error("No response body");

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let isFirstToken = true;

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n\n');

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        try {
                            const jsonStr = line.slice(6);
                            if (!jsonStr) continue;

                            const data = JSON.parse(jsonStr);

                            if (data.token) {
                                if (isFirstToken) {
                                    setIsLoading(false);
                                    isFirstToken = false;
                                }

                                setMessages(prev => prev.map(msg =>
                                    msg.id === aiMsgId
                                        ? { ...msg, content: msg.content + data.token }
                                        : msg
                                ));
                            }

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
        <div className="h-screen flex bg-[#09090b] text-zinc-100 font-sans overflow-hidden selection:bg-white/20">

            {/* Left Sidebar Wrapper */}
            <div className={`transition-all duration-300 ease-in-out border-zinc-800 flex-shrink-0 relative ${isLeftOpen ? 'w-64' : 'w-0 border-none'}`}>
                <div className="w-64 h-full">
                    <SidebarLeft docMode={docMode} setDocMode={setDocMode} onModeSwitch={() => setMessages([])} />
                </div>
            </div>

            {/* Main Content */}
            <main className="flex-1 flex flex-col relative h-full min-w-0 bg-[#09090b]">
                <ChatHeader
                    activeMode={activeMode}
                    isLeftOpen={isLeftOpen}
                    toggleLeft={() => setIsLeftOpen(!isLeftOpen)}
                    isRightOpen={isRightOpen}
                    toggleRight={() => setIsRightOpen(!isRightOpen)}
                />

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

            {/* Right Sidebar Wrapper */}
            <div className={`transition-all duration-300 ease-in-out border-zinc-800 flex-shrink-0 relative hidden xl:block ${isRightOpen ? 'w-72' : 'w-0 border-none'}`}>
                <div className="w-72 h-full">
                    <SidebarRight activeMode={activeMode} />
                </div>
            </div>

        </div>
    );
}