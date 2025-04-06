"use client"

import React, { useState } from "react"
// @ts-ignore - lucide-react doesn't have type definitions
import { Copy, Check, Lightbulb, Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useSyntax } from "@/contexts/SyntaxContext"
import { SyntaxItem } from "@/types"

// Define proper types for our component

export function SyntaxResults() {
  const { filteredItems, copyToClipboard, copiedText } = useSyntax()
  const [explainItem, setExplainItem] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Results</h2>
        <span className="text-sm text-slate-400">
          Showing {filteredItems.length} result{filteredItems.length !== 1 ? 's' : ''}
        </span>
      </div>

      {filteredItems.length === 0 ? (
        <div className="flex flex-col items-center justify-center rounded-lg border border-slate-800 bg-slate-900 p-8 text-center">
          <div className="mb-4 rounded-full bg-slate-800 p-3">
            <Search className="h-6 w-6 text-slate-400" />
          </div>
          <h3 className="mb-2 text-lg font-medium text-white">No results found</h3>
          <p className="text-slate-400">Try adjusting your search or filter criteria</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredItems.map((item: SyntaxItem) => (
            <div
              key={item.id}
              className="group relative overflow-hidden rounded-lg border border-slate-800 bg-slate-900 shadow-md transition-all duration-300 hover:border-cyan-900/50 hover:shadow-[0_0_15px_rgba(0,200,255,0.15)]"
            >
              <div className="absolute inset-x-0 top-0 h-0.5 bg-gradient-to-r from-cyan-500 to-purple-500 opacity-0 transition-opacity duration-300 group-hover:opacity-100"></div>

              <div className="flex flex-col gap-3 p-4">
                <div className="flex items-start justify-between">
                  <Badge
                    variant="outline"
                    className="border-purple-500/30 bg-purple-950/30 text-purple-400"
                  >
                    {item.category}
                  </Badge>

                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 rounded-full bg-slate-800/50 text-slate-400 hover:bg-cyan-900/50 hover:text-cyan-400"
                    onClick={() => copyToClipboard(item.command)}
                    title="Copy command"
                  >
                    {copiedText === item.command ? (
                      <Check className="h-4 w-4" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </Button>
                </div>

                <div>
                  <h3 className="mb-1 font-mono text-lg font-bold text-white">
                    {item.command}
                  </h3>
                  <p className="text-sm text-slate-400">{item.description}</p>
                </div>

                <div className="flex flex-wrap gap-2 pt-2">
                  {item.tags.map((tag: string) => (
                    <Badge
                      key={tag}
                      variant="secondary"
                      className="bg-slate-800 text-xs text-slate-300 hover:bg-slate-700"
                    >
                      {tag}
                    </Badge>
                  ))}
                </div>

                <Button
                  variant="ghost"
                  size="sm"
                  className="mt-2 flex w-full items-center justify-center gap-1 rounded-md border border-cyan-900/30 bg-cyan-950/20 py-1 text-xs text-cyan-400 hover:bg-cyan-900/30"
                  onClick={() => setExplainItem(explainItem === item.id ? null : item.id)}
                >
                  <Lightbulb className="h-3 w-3" />
                  Explain with AI
                </Button>

                {explainItem === item.id && (
                  <div className="mt-2 rounded-md bg-slate-800/50 p-3 text-xs text-slate-300">
                    <p className="italic text-slate-400">
                      AI explanation would appear here...
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

