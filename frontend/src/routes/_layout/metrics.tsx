import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Suspense } from "react"

import { client } from "@/client/client.gen"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { ensurePermission } from "@/lib/permissions"

type Metrics = {
  user_count: number
  users_by_role: Record<string, number>
}

async function readMetrics(): Promise<Metrics> {
  const { data } = await client.get<{ 200: Metrics }>({
    responseType: "json",
    security: [{ scheme: "bearer", type: "http" }],
    url: "/api/v1/metrics/",
  })
  if (!data) {
    throw new Error("Metrics response was empty")
  }
  return data
}

export const Route = createFileRoute("/_layout/metrics")({
  component: MetricsPage,
  beforeLoad: () => ensurePermission("metrics:view"),
  head: () => ({
    meta: [{ title: "Metrics - FastAPI Template" }],
  }),
})

function MetricsContent() {
  const { data } = useSuspenseQuery({
    queryKey: ["metrics"],
    queryFn: readMetrics,
  })
  const counts = [
    { label: "Users", value: data.user_count },
    { label: "Admins", value: data.users_by_role.admin ?? 0 },
    { label: "Managers", value: data.users_by_role.manager ?? 0 },
    { label: "Members", value: data.users_by_role.member ?? 0 },
  ]

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {counts.map((item) => (
        <Card key={item.label}>
          <CardHeader>
            <CardDescription>{item.label}</CardDescription>
            <CardTitle className="text-3xl">{item.value}</CardTitle>
          </CardHeader>
          <CardContent />
        </Card>
      ))}
    </div>
  )
}

function MetricsPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Metrics</h1>
        <p className="text-muted-foreground">
          How many people are in each role.
        </p>
      </div>
      <Suspense fallback={<p className="text-muted-foreground">Loading metrics…</p>}>
        <MetricsContent />
      </Suspense>
    </div>
  )
}
