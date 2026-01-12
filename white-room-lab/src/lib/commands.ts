/**
 * Command parsing for White Room Lab chat interface
 */

import { FormType } from './transforms';

export interface ParsedCommand {
  intent: 'transform' | 'create' | 'move' | 'delete' | 'help' | 'unknown';
  target?: string;
  parameters?: Record<string, any>;
}

/**
 * Parse natural language commands
 */
export function parseCommand(input: string): ParsedCommand {
  const lower = input.toLowerCase().trim();

  // Transform commands
  const transformKeywords = ['verwandel', 'transform', 'werde', 'become', 'zeig', 'show', 'mach', 'make'];
  if (transformKeywords.some(kw => lower.includes(kw))) {
    // Extract target form
    const target = lower
      .replace(/verwandel(e|t)?\s+(dich\s+)?in\s+/gi, '')
      .replace(/transform\s+(to|into)\s+/gi, '')
      .replace(/werde\s+(zu\s+)?/gi, '')
      .replace(/become\s+(a\s+)?/gi, '')
      .replace(/zeig(e)?\s+(mir\s+)?/gi, '')
      .replace(/show\s+(me\s+)?/gi, '')
      .replace(/mach(e)?\s+/gi, '')
      .replace(/make\s+(a\s+)?/gi, '')
      .trim();

    return {
      intent: 'transform',
      target,
    };
  }

  // Create commands
  const createKeywords = ['erstell', 'create', 'bau', 'build'];
  if (createKeywords.some(kw => lower.includes(kw))) {
    return {
      intent: 'create',
      target: lower,
    };
  }

  // Help commands
  const helpKeywords = ['hilfe', 'help', 'was kannst du', 'what can you'];
  if (helpKeywords.some(kw => lower.includes(kw))) {
    return {
      intent: 'help',
    };
  }

  return {
    intent: 'unknown',
    target: input,
  };
}

/**
 * Map natural language targets to form types
 */
export function mapTargetToForm(target: string): FormType | null {
  const lower = target.toLowerCase();

  // DNA
  if (lower.match(/dna|helix|gen|genetisch/)) {
    return 'dna';
  }

  // Neural Network
  if (lower.match(/neural|netzwerk|network|gehirn|brain|ai|ki/)) {
    return 'neural';
  }

  // Molecule
  if (lower.match(/molekül|molecule|wasser|water|h2o|chemie|chemistry/)) {
    return 'molecule';
  }

  // City
  if (lower.match(/stadt|city|gebäude|building|urban/)) {
    return 'city';
  }

  // Galaxy
  if (lower.match(/galaxie|galaxy|sterne|stars|weltraum|space|kosmos|cosmos/)) {
    return 'galaxy';
  }

  // Turbine
  if (lower.match(/turbine|windrad|wind|energie|energy/)) {
    return 'turbine';
  }

  // Tool
  if (lower.match(/werkzeug|tool|hammer|schraub/)) {
    return 'tool';
  }

  // Vehicle
  if (lower.match(/fahrzeug|vehicle|auto|car|wagen/)) {
    return 'vehicle';
  }

  // Human
  if (lower.match(/mensch|human|person|körper|body/)) {
    return 'human';
  }

  // Bugs Bunny
  if (lower.match(/bugs|bunny|hase|rabbit|cartoon/)) {
    return 'bugs_bunny';
  }

  // Bubble (default)
  if (lower.match(/bubble|blase|ball|kugel|sphere/)) {
    return 'bubble';
  }

  return null;
}

/**
 * Get help text for available commands
 */
export function getHelpText(): string {
  return `
**Verfügbare Befehle / Available Commands:**

**Transformationen:**
- "Verwandle dich in DNA" → DNA Helix
- "Zeig mir ein neuronales Netzwerk" → Neural Network
- "Werde zu einem Wassermolekül" → H2O Molecule
- "Bau eine Stadt" → Procedural City
- "Zeig mir eine Galaxie" → Spiral Galaxy
- "Werde zu einem Menschen" → Human Form

**Weitere:**
- "Hilfe" / "Help" → Diese Nachricht
- "Was kannst du?" → Zeige Fähigkeiten

Spreche natürlich! Ich verstehe Deutsch und Englisch.
  `.trim();
}
