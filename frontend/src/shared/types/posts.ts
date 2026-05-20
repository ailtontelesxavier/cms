import type { Tag } from './tags'

export type PostStatus = 'draft' | 'review' | 'published' | 'archived'

export interface Post {
  id: string
  title: string
  slug: string
  status: PostStatus
  author_id: string
  published_at: string | null
  created_at: string
  updated_at: string
  tags: Tag[]
}

export interface PostContent {
  html: string
  plain_text: string
  summary: string
  cover_image: Record<string, unknown> | null
  images: Record<string, unknown>[]
}

export interface PostDetail extends Post {
  content: PostContent | null
}

export interface PostCreate {
  title: string
  slug: string
  html: string
  summary?: string
  tag_ids?: number[]
}

export interface PostUpdate {
  title?: string
  html?: string
  summary?: string
  tag_ids?: number[]
}

export interface ImageUploadResult {
  image_id: string
  object_key: string
  url: string
}
