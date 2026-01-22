import { LucideIcon } from 'lucide-react';

export type DocMode = 'langchain' | 'stripe' | 'jira'; //  | 'notion'

export interface Source {
  title: string;
  url: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  timestamp: number;
}

export interface DocContext {
  version: string;
  baseUrl: string;
  authType: string;
  popularEndpoints: string[];
  documentationUrl: string;
}

export interface ModeConfig {
  name: string; 
  description: string;
  color: string; 
  icon: LucideIcon; 
  suggestions: string[];
  context: DocContext;
}