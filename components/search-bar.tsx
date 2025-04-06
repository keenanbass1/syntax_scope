"use client"

import React from "react"
// @ts-ignore - lucide-react doesn't have type definitions
import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useSyntax } from "@/contexts/SyntaxContext"

export function SearchBar() {
  const { searchQuery, setSearchQuery } = useSyntax()

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Search form submitted with query:", searchQuery)
    // Search is already handled automatically via context
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log("Search input changing to:", e.target.value)
    setSearchQuery(e.target.value)
  }

  return (
    <form onSubmit={handleSearch} className="mb-8">
      <div className="relative">
        <div className="group relative rounded-lg border border-slate-700 bg-slate-900 shadow-[0_0_15px_rgba(0,200,255,0.15)] transition-all duration-300 focus-within:border-cyan-500 focus-within:shadow-[0_0_20px_rgba(0,200,255,0.3)] hover:border-slate-600">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
            <Search className="h-5 w-5 text-slate-400 group-focus-within:text-cyan-400" />
          </div>
          <Input
            type="text"
            placeholder="Search commands (e.g., 'list files', 'process management', 'find text')"
            value={searchQuery}
            onChange={handleInputChange}
            className="h-14 border-0 bg-transparent pl-12 pr-24 text-lg text-white placeholder:text-slate-500 focus-visible:ring-0 focus-visible:ring-offset-0"
          />
          <div className="absolute inset-y-0 right-0 flex items-center pr-3">
            <Button
              type="submit"
              className="h-10 bg-gradient-to-r from-cyan-600 to-purple-600 text-white hover:from-cyan-500 hover:to-purple-500"
            >
              Search
            </Button>
          </div>
        </div>
        <div className="mt-2 text-xs text-slate-500">
          <span className="font-medium text-cyan-400">Pro tip:</span> Use fuzzy search like &quot;ls -la&quot; or
          &quot;find all files&quot;
        </div>
      </div>
    </form>
  )
}

