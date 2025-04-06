import { SearchBar } from "@/components/search-bar"
import { ShellFilter } from "@/components/shell-filter"
import { SyntaxResults } from "@/components/syntax-results"
import { FutureFeatures } from "@/components/future-features"
import { Header } from "@/components/header"
import { SyntaxProvider } from "@/contexts/SyntaxContext"
import React from "react"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <Header />
      <main className="container mx-auto px-4 pb-16 pt-24">
        <div className="mx-auto max-w-4xl">
          <h1 className="mb-6 text-center text-4xl font-bold tracking-tighter text-white md:text-5xl lg:text-6xl">
            <span className="bg-gradient-to-r from-cyan-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent">
              SyntaxScope
            </span>
          </h1>
          <p className="mb-8 text-center text-lg text-slate-400">
            Search and discover command syntax across multiple shells
          </p>
          <SyntaxProvider>
            {/* @ts-ignore - Children prop is properly passed */}
            <SearchBar />
            <ShellFilter />
            <SyntaxResults />
          </SyntaxProvider>
          <FutureFeatures />
        </div>
      </main>
    </div>
  )
}
