export interface Tag {
  id: number
  name: string
  description: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface TagCreate {
  name: string
  description?: string | null
}

export interface TagUpdate {
  name?: string
  description?: string | null
}
