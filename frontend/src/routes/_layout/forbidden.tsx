import { createFileRoute, Link } from "@tanstack/react-router"

import { Button } from "@/components/ui/button"

export const Route = createFileRoute("/_layout/forbidden")({
  component: Forbidden,
  head: () => ({
    meta: [{ title: "Access Denied - FastAPI Template" }],
  }),
})

function Forbidden() {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center text-center">
      <h1 className="text-3xl font-bold tracking-tight">Access Denied</h1>
      <p className="mt-2 max-w-md text-muted-foreground">
        You do not have permission to view this page. If you think this is a
        mistake, ask an admin to change your role.
      </p>
      <Button asChild className="mt-6">
        <Link to="/">Back to dashboard</Link>
      </Button>
    </div>
  )
}
