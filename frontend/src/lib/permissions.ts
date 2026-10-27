import { redirect } from "@tanstack/react-router"

import { UsersService } from "@/client"

export const ROLES = ["admin", "manager", "member"] as const

export type RoleName = (typeof ROLES)[number]

export function isRole(value: string): value is RoleName {
  return ROLES.some((role) => role === value)
}

export function hasPermission(
  user: { permissions?: readonly string[] } | null | undefined,
  permission: string,
): boolean {
  return user?.permissions?.includes(permission) ?? false
}

export async function ensurePermission(permission: string): Promise<void> {
  const { data: user } = await UsersService.readUserMe()
  if (!hasPermission(user, permission)) {
    throw redirect({ to: "/forbidden" })
  }
}
