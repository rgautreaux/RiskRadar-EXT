// Utility to fetch and search documentation (e.g., USER_GUIDE.md) for Golby
// This can be extended to support more docs later.

export async function fetchUserGuide(): Promise<string> {
  const res = await fetch('/USER_GUIDE.md');
  if (!res.ok) throw new Error('Failed to fetch USER_GUIDE.md');
  return await res.text();
}

export function searchDocForAnswer(doc: string, query: string): string {
  // Simple keyword search: return the first matching section or a fallback
  const lowerDoc = doc.toLowerCase();
  const lowerQuery = query.toLowerCase();
  // Try to find a section containing the query
  const lines = doc.split('\n');
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].toLowerCase().includes(lowerQuery)) {
      // Return the matching line and a few lines after for context
      return lines.slice(i, i + 5).join('\n');
    }
  }
  return "Sorry, I couldn't find an answer in the documentation.";
}
