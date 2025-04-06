"use client"

import { useState } from "react"
import { Copy, Check, ExternalLink } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

// Mock data for demonstration
const mockResults = [
  {
    id: 1,
    command: "ls -la",
    description: "List all files in long format, including hidden files",
    shell: "bash",
    syntax: "ls [options] [file/directory]",
    example: "ls -la /home/user",
    tags: ["files", "directory", "listing"],
  },
  {
    id: 2,
    command: "find . -name '*.js'",
    description: "Find all JavaScript files in the current directory and subdirectories",
    shell: "bash",
    syntax: "find [path] [expression]",
    example: "find . -name '*.js' -type f",
    tags: ["search", "files", "pattern"],
  },
  {
    id: 3,
    command: "ps aux | grep node",
    description: "Find all running Node.js processes",
    shell: "bash",
    syntax: "ps [options] | grep [pattern]",
    example: "ps aux | grep node",
    tags: ["process", "filter", "search"],
  },
]

export function SyntaxResults() {
  const [copiedId, setCopiedId] = useState<number | null>(null)

  const copyToClipboard = (text: string, id: number) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Results</h2>
        <span className="text-sm text-slate-400">Showing {mockResults.length} results</span>
      </div>

      {mockResults.map((result) => (
        <div
          key={result.id}
          className="group relative overflow-hidden rounded-lg border border-slate-800 bg-slate-900 shadow-md transition-all duration-300 hover:border-cyan-900/50 hover:shadow-[0_0_15px_rgba(0,200,255,0.15)]"
        >
          <div className="flex flex-col gap-4 p-5">
            <div className="flex flex-wrap items-start justify-between gap-2">
              <div>
                <h3 className="text-lg font-bold text-white">{result.command}</h3>
                <p className="mt-1 text-sm text-slate-400">{result.description}</p>
              </div>
              <Badge variant="outline" className="border-purple-500/30 bg-purple-950/30 text-purple-400">
                {result.shell}
              </Badge>
            </div>

            <div className="rounded-md bg-slate-950 p-4">
              <div className="mb-2 flex items-center justify-between">
                <span className="text-xs font-medium text-slate-500">Syntax</span>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6 text-slate-500 hover:text-cyan-400"
                  onClick={() => copyToClipboard(result.syntax, result.id)}
                >
                  {copiedId === result.id ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                </Button>
              </div>
              <pre className="overflow-x-auto text-sm text-cyan-400">
                <code>{result.syntax}</code>
              </pre>
            </div>

            <div className="rounded-md bg-slate-950 p-4">
              <div className="mb-2 flex items-center justify-between">
                <span className="text-xs font-medium text-slate-500">Example</span>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6 text-slate-500 hover:text-cyan-400"
                  onClick={() => copyToClipboard(result.example, result.id + 100)}
                >
                  {copiedId === result.id + 100 ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                </Button>
              </div>
              <pre className="overflow-x-auto text-sm text-green-400">
                <code>{result.example}</code>
              </pre>
            </div>

            <div className="flex flex-wrap gap-2">
              {result.tags.map((tag) => (
                <Badge key={tag} variant="secondary" className="bg-slate-800 text-slate-300 hover:bg-slate-700">
                  {tag}
                </Badge>
              ))}
            </div>

            <Button
              variant="link"
              className="ml-auto flex items-center gap-1 p-0 text-xs text-cyan-400 hover:text-cyan-300"
            >
              View details
              <ExternalLink className="h-3 w-3" />
            </Button>
          </div>
          <div className="absolute inset-x-0 top-0 h-0.5 bg-gradient-to-r from-cyan-500 to-purple-500 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>
        </div>
      ))}
    </div>
  )
}

