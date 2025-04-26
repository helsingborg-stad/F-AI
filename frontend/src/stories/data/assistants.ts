import type { IAssistant } from '$lib/types.js'

export const mockAssistants: IAssistant[] = [
  {
    id: '6808ddaffcd3461eea42133f',
    owner: 'user@example.com',
    name: 'Research Assistant',
    description: 'Helps with research tasks and information gathering',
    instructions: 'Answer questions clearly and cite sources when possible',
    model: 'gpt-4',
  },
  {
    id: '6651afc3a7b5e3c8d9f01234',
    owner: 'user@example.com',
    name: 'Code Helper',
    description: 'Provides coding assistance and debugging help',
    instructions: 'Explain code solutions with comments for clarity',
    model: 'claude-3',
  },
]
