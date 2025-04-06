"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react"
// @ts-ignore - Fuse.js doesn't have type definitions
import Fuse from "fuse.js"
import { SyntaxItem } from "@/types"

type SyntaxContextType = {
  syntaxItems: SyntaxItem[]
  filteredItems: SyntaxItem[]
  searchQuery: string
  activeCategory: string | null
  setSearchQuery: (query: string) => void
  setActiveCategory: (category: string | null) => void
  copyToClipboard: (text: string) => void
  copiedText: string | null
}

const SyntaxContext = createContext<SyntaxContextType | undefined>(undefined)

// Simple fallback search function when Fuse.js fails
const manualSearch = (items: SyntaxItem[], query: string): SyntaxItem[] => {
  const searchTerms = query.toLowerCase().trim().split(/\s+/);
  return items.filter(item => {
    const command = item.command.toLowerCase();
    const description = item.description.toLowerCase();
    const tags = item.tags.join(' ').toLowerCase();
    const searchText = `${command} ${description} ${tags}`;
    
    // Item matches if all search terms are found somewhere in the searchable text
    return searchTerms.every(term => searchText.includes(term));
  });
};

export function SyntaxProvider({ children }: { children: ReactNode }) {
  const [syntaxItems, setSyntaxItems] = useState<SyntaxItem[]>([])
  const [filteredItems, setFilteredItems] = useState<SyntaxItem[]>([])
  const [searchQuery, setSearchQuery] = useState("")
  const [activeCategory, setActiveCategory] = useState<string | null>(null)
  const [copiedText, setCopiedText] = useState<string | null>(null)
  // @ts-ignore - Fuse type issues
  const [fuse, setFuse] = useState<any>(null)

  // Load syntax data
  useEffect(() => {
    const loadSyntaxData = async () => {
      try {
        console.log("Fetching syntax data...")
        const response = await fetch("/data/syntax.json")
        
        if (!response.ok) {
          throw new Error(`Failed to fetch syntax data: ${response.status} ${response.statusText}`)
        }
        
        const data = await response.json()
        console.log("Syntax data loaded:", data)
        setSyntaxItems(data)
        setFilteredItems(data)

        // Initialize Fuse instance with more relaxed options
        // @ts-ignore - Ignore Fuse typing issues
        const fuseInstance = new Fuse(data, {
          keys: ["command", "description", "tags"],
          includeScore: true,
          includeMatches: true,
          threshold: 0.3,           // Lower threshold = more strict matching
          location: 0,              // Where to start searching in the string
          distance: 100,            // How far to search for a match (higher = more permissive)
          minMatchCharLength: 2,    // Minimum length of characters to consider as a match
          shouldSort: true,         // Sort by score
          findAllMatches: true,
          ignoreLocation: true,     // Ignore location and distance altogether
        })
        setFuse(fuseInstance)
        console.log("Fuse instance created")
      } catch (error) {
        console.error("Error loading syntax data:", error)
      }
    }

    loadSyntaxData()
  }, [])

  // Filter items based on search query and category
  useEffect(() => {
    console.log("Filter effect running with:", { searchQuery, activeCategory, itemsCount: syntaxItems.length })
    
    // Exit early if no items yet
    if (!syntaxItems.length) {
      console.log("No items to filter yet")
      return
    }
    
    let results: SyntaxItem[] = [...syntaxItems]
    
    // First, apply search if query exists
    if (searchQuery && searchQuery.trim() !== "") {
      try {
        // Try Fuse.js search first
        if (fuse) {
          console.log("Searching with Fuse for:", searchQuery)
          const searchResults = fuse.search(searchQuery)
          console.log("Fuse results:", searchResults)
          
          if (searchResults.length > 0) {
            // Extract items from search results
            results = searchResults.map((result: any) => result.item)
          } else {
            console.log("No Fuse results, trying manual search")
            // If no results, try manual search as fallback
            results = manualSearch(syntaxItems, searchQuery);
          }
        } else {
          // If Fuse not available, use manual search
          console.log("Fuse not available, using manual search")
          results = manualSearch(syntaxItems, searchQuery);
        }
        
        console.log("Search yielded", results.length, "results")
      } catch (error) {
        console.error("Error during search:", error)
        // If search fails, try manual search
        results = manualSearch(syntaxItems, searchQuery);
      }
    }
    
    // Then apply category filter if needed
    if (activeCategory) {
      console.log("Filtering by category:", activeCategory)
      results = results.filter(item => item.category === activeCategory)
    }
    
    console.log("Final filtered results:", results.length)
    setFilteredItems(results)
  }, [searchQuery, activeCategory, syntaxItems, fuse])

  // Copy to clipboard function
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    setCopiedText(text)
    setTimeout(() => setCopiedText(null), 2000)
  }

  const value = {
    syntaxItems,
    filteredItems,
    searchQuery,
    activeCategory,
    setSearchQuery,
    setActiveCategory,
    copyToClipboard,
    copiedText
  }

  return <SyntaxContext.Provider value={value}>{children}</SyntaxContext.Provider>
}

export function useSyntax() {
  const context = useContext(SyntaxContext)
  if (context === undefined) {
    throw new Error("useSyntax must be used within a SyntaxProvider")
  }
  return context
}