"use client"

import React from "react"
// @ts-ignore - lucide-react doesn't have type definitions
import { Terminal, Hash, Code, Braces } from "lucide-react"
import { useSyntax } from "@/contexts/SyntaxContext"

export function ShellFilter() {
  const { activeCategory, setActiveCategory } = useSyntax()

  const shells = [
    { id: "bash", name: "Bash", icon: Terminal },
    { id: "zsh", name: "Zsh", icon: Hash },
    { id: "powershell", name: "PowerShell", icon: Code },
    { id: "python", name: "Python", icon: Braces },
  ] as const

  return (
    <div className="mb-8">
      <div className="flex flex-wrap justify-center gap-2 rounded-lg border border-slate-800 bg-slate-900/50 p-1">
        {shells.map((shell) => (
          <button
            key={shell.id}
            onClick={() => setActiveCategory(activeCategory === shell.id ? null : shell.id)}
            className={`flex items-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-all ${
              activeCategory === shell.id
                ? "bg-gradient-to-r from-cyan-900/50 to-purple-900/50 text-white shadow-[0_0_10px_rgba(0,200,255,0.2)]"
                : "text-slate-400 hover:bg-slate-800 hover:text-white"
            }`}
          >
            <shell.icon className="h-4 w-4" />
            {shell.name}
          </button>
        ))}
      </div>
    </div>
  )
}

