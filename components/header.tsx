"use client"

import { useState } from "react"
import Link from "next/link"
import { Terminal, MessageSquare, Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { FeedbackDialog } from "./feedback-dialog"

export function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const [feedbackOpen, setFeedbackOpen] = useState(false)

  return (
    <header className="fixed top-0 z-50 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold text-white">
          <Terminal className="h-6 w-6 text-cyan-400" />
          <span className="bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
            SyntaxScope
          </span>
        </Link>

        <div className="hidden items-center gap-6 md:flex">
          <nav className="flex items-center gap-4">
            <Link href="#" className="text-sm text-slate-400 transition-colors hover:text-white">
              Documentation
            </Link>
            <Link href="#" className="text-sm text-slate-400 transition-colors hover:text-white">
              API
            </Link>
            <Link href="#" className="text-sm text-slate-400 transition-colors hover:text-white">
              About
            </Link>
          </nav>
          <Button
            variant="outline"
            size="sm"
            className="border-cyan-500/50 bg-transparent text-cyan-400 hover:bg-cyan-950 hover:text-cyan-300"
            onClick={() => setFeedbackOpen(true)}
          >
            <MessageSquare className="mr-2 h-4 w-4" />
            Feedback
          </Button>
        </div>

        <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X className="h-5 w-5 text-slate-400" /> : <Menu className="h-5 w-5 text-slate-400" />}
        </Button>

        {isOpen && (
          <div className="absolute left-0 top-16 z-50 w-full border-b border-slate-800 bg-slate-950 p-4 md:hidden">
            <nav className="flex flex-col gap-4">
              <Link href="#" className="text-sm text-slate-400 transition-colors hover:text-white">
                Documentation
              </Link>
              <Link href="#" className="text-sm text-slate-400 transition-colors hover:text-white">
                API
              </Link>
              <Link href="#" className="text-sm text-slate-400 transition-colors hover:text-white">
                About
              </Link>
              <Button
                variant="outline"
                size="sm"
                className="mt-2 w-full border-cyan-500/50 bg-transparent text-cyan-400 hover:bg-cyan-950 hover:text-cyan-300"
                onClick={() => {
                  setFeedbackOpen(true)
                  setIsOpen(false)
                }}
              >
                <MessageSquare className="mr-2 h-4 w-4" />
                Feedback
              </Button>
            </nav>
          </div>
        )}

        <FeedbackDialog open={feedbackOpen} setOpen={setFeedbackOpen} />
      </div>
    </header>
  )
}

