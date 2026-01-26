import { Layers, Terminal, FileText, BookOpen } from 'lucide-react';
import { DocMode, ModeConfig } from '@/types/types';

export const MOCK_MODES: Record<DocMode, ModeConfig> = {
    langchain: {
        name: 'LangChain',
        description: 'Framework for LLM apps',
        color: 'text-emerald-400',
        icon: Layers,
        suggestions: ["How to create a retriever?", "Difference: invoke vs stream", "Using format_documents for RAG"],
        context: {
            version: "v0.1.0",
            baseUrl: "docs.langchain.com",
            authType: "None (Open Source)",
            popularEndpoints: ["integrations.retrievers", "integrations.document_loaders", "integrations.text_splitters"],
            documentationUrl: "https://docs.langchain.com/"
        }
    },
    stripe: {
        name: 'Stripe API',
        description: 'Payment infrastructure',
        color: 'text-indigo-400',
        icon: Terminal,
        suggestions: ["Create a PaymentIntent", "Handle subscription webhooks", "List active customers"],
        context: {
            version: "2023-10-16",
            baseUrl: "api.stripe.com/v1",
            authType: "Bearer <sk_key>",
            popularEndpoints: ["/payment_intents", "/customers", "/checkout/sessions"],
            documentationUrl: "https://docs.stripe.com/"
        },
    },
    jira: {
        name: 'Jira Cloud',
        description: 'Issue tracking API',
        color: 'text-blue-400',
        icon: FileText,
        suggestions: ["Search issues with JQL", "Transition workflow status", "Get project details"],
        context: {
            version: "v3",
            baseUrl: "your-domain.atlassian.net",
            authType: "Basic Auth (Email + Token)",
            popularEndpoints: ["/search", "/issue/{key}", "/myself"],
            documentationUrl: "https://confluence.atlassian.com/jira"
        },
    },
    // notion: {
    //     name: 'Notion',
    //     description: 'Workspace & notes API',
    //     color: 'text-zinc-200',
    //     icon: BookOpen,
    //     suggestions: ["Query database with filters", "Append children blocks", "Retrieve user info"],
    //     context: {
    //         version: "2022-06-28",
    //         baseUrl: "api.notion.com/v1",
    //         authType: "Bearer <secret>",
    //         popularEndpoints: ["/pages", "/databases/{id}/query", "/blocks"]
    //     }
    // }
};