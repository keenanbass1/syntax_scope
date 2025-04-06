import { Sparkles, Save, Brain, GitCompare } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function FutureFeatures() {
  const features = [
    {
      title: "Save Snippets",
      description: "Save your favorite commands for quick access",
      icon: Save,
      comingSoon: true,
    },
    {
      title: "AI Explain",
      description: "Get AI-powered explanations of complex commands",
      icon: Brain,
      comingSoon: true,
    },
    {
      title: "Compare Syntax",
      description: "Compare command syntax across different shells",
      icon: GitCompare,
      comingSoon: true,
    },
  ]

  return (
    <div className="mt-16">
      <div className="mb-6 flex items-center gap-2">
        <Sparkles className="h-5 w-5 text-purple-400" />
        <h2 className="text-xl font-bold text-white">Coming Soon</h2>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {features.map((feature) => (
          <Card
            key={feature.title}
            className="border-slate-800 bg-slate-900/50 transition-all duration-300 hover:border-purple-900/50 hover:shadow-[0_0_15px_rgba(149,76,233,0.15)]"
          >
            <CardHeader className="pb-2">
              <div className="mb-2 flex h-8 w-8 items-center justify-center rounded-full bg-purple-950/50 text-purple-400">
                <feature.icon className="h-4 w-4" />
              </div>
              <CardTitle className="text-white">{feature.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-slate-400">{feature.description}</CardDescription>
              {feature.comingSoon && (
                <span className="mt-3 inline-block rounded-full bg-purple-950/30 px-2 py-0.5 text-xs text-purple-400">
                  Coming soon
                </span>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

