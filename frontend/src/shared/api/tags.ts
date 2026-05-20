import client from './client'
import type { PaginatedResult } from '@/shared/types/api'
import type { Tag, TagCreate, TagUpdate } from '@/shared/types/tags'

export const tagsApi = {
  list(page = 1, pageSize = 20) {
    return client.get<PaginatedResult<Tag>>('/tags', { params: { page, page_size: pageSize } })
  },

  getById(id: number) {
    return client.get<Tag>(`/tags/${id}`)
  },

  create(data: TagCreate) {
    return client.post<Tag>('/tags', data)
  },

  update(id: number, data: TagUpdate) {
    return client.patch<Tag>(`/tags/${id}`, data)
  },

  delete(id: number) {
    return client.delete(`/tags/${id}`)
  },
}
