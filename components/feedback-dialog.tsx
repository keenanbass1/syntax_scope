"use client"

import type React from "react"

import { useState } from "react"
import { MessageSquare } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Check } from "lucide-react"

interface FeedbackDialogProps {
  open: boolean
  setOpen: (open: boolean) => void
}

export function FeedbackDialog({ open, setOpen }: FeedbackDialogProps) {
  const [feedback, setFeedback] = useState("")
  const [email, setEmail] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Simulate API call
    setTimeout(() => {
      console.log("Feedback submitted:", { feedback, email })
      setIsSubmitting(false)
      setIsSubmitted(true)

      // Reset form after 2 seconds and close dialog
      setTimeout(() => {
        setFeedback("")
        setEmail("")
        setIsSubmitted(false)
        setOpen(false)
      }, 2000)
    }, 1000)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="border-slate-800 bg-slate-950 text-white sm:max-w-md">
        <DialogHeader>
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-cyan-950/50">
            <MessageSquare className="h-6 w-6 text-cyan-400" />
          </div>
          <DialogTitle className="text-center text-xl">Send Feedback</DialogTitle>
          <DialogDescription className="text-center text-slate-400">
            Help us improve SyntaxScope with your suggestions
          </DialogDescription>
        </DialogHeader>

        {isSubmitted ? (
          <div className="flex flex-col items-center justify-center py-6">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-950/50">
              <Check className="h-8 w-8 text-green-400" />
            </div>
            <p className="text-center text-lg font-medium text-white">Thank you for your feedback!</p>
            <p className="text-center text-slate-400">
              We appreciate your input and will use it to improve SyntaxScope.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="space-y-4 py-2">
              <div className="space-y-2">
                <Label htmlFor="feedback">Your feedback</Label>
                <Textarea
                  id="feedback"
                  placeholder="Share your thoughts, ideas, or report issues..."
                  value={feedback}
                  onChange={(e) => setFeedback(e.target.value)}
                  className="min-h-32 border-slate-800 bg-slate-900 text-white placeholder:text-slate-500 focus-visible:ring-cyan-500"
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email (optional)</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="your@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="border-slate-800 bg-slate-900 text-white placeholder:text-slate-500 focus-visible:ring-cyan-500"
                />
                <p className="text-xs text-slate-500">We'll only use this to follow up on your feedback if needed</p>
              </div>
            </div>
            <DialogFooter className="mt-6">
              <Button
                type="button"
                variant="outline"
                onClick={() => setOpen(false)}
                className="border-slate-700 bg-transparent text-slate-300 hover:bg-slate-900 hover:text-white"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={isSubmitting || !feedback}
                className="bg-gradient-to-r from-cyan-600 to-purple-600 text-white hover:from-cyan-500 hover:to-purple-500"
              >
                {isSubmitting ? "Sending..." : "Send Feedback"}
              </Button>
            </DialogFooter>
          </form>
        )}
      </DialogContent>
    </Dialog>
  )
}

