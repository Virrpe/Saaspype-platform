# Luciq Persona Activation System

## Overview
This system allows activation of specialized AI personas for specific development tasks.

## Available Personas

### RefactorArchitect
**Activation Command**: `activate refactoring specialist`
**Configuration File**: `working-memory/refactoring-specialist-persona.json`
**Specialization**: Memory-aware, V2-compliant code optimization

## Activation Protocol

When user types any of the activation commands, the system should:

1. Load the corresponding persona configuration from working-memory
2. Display the activation response from the persona config
3. Switch context to operate under that persona's constraints and mission
4. Begin executing the persona's task framework

## Command Mapping

| User Input | Persona | Config File |
|------------|---------|-------------|
| `activate refactoring specialist` | RefactorArchitect | `refactoring-specialist-persona.json` |

## Implementation Notes

- Personas maintain awareness of current project state (150% completion)
- All personas respect the existing memory system and session continuity
- Safety rules prevent breaking production features
- Each persona has a structured task framework for consistent execution

## Future Personas

Additional personas can be added by:
1. Creating a new persona config JSON file in working-memory/
2. Adding the activation command to this mapping
3. Defining the persona's mission, constraints, and task framework 