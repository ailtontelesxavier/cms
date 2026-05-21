import client from './client'
import type { PaginatedResult } from '@/shared/types/api'
import type { Post, PostCreate, PostUpdate, ImageUploadResult } from '@/shared/types/posts'

export const postsApi = {
  list(page = 1, pageSize = 20, status?: string, q?: string) {
    return client.get<PaginatedResult<Post>>('/posts', {
      params: { page, page_size: pageSize, ...(status ? { status } : {}), ...(q ? { q } : {}) },
    })
  },

  getById(id: string) {
    return client.get<Post>(`/posts/${id}`)
  },

  create(data: PostCreate) {
    return client.post<Post>('/posts', data)
  },

  update(id: string, data: PostUpdate) {
    return client.patch<Post>(`/posts/${id}`, data)
  },

  publish(id: string) {
    return client.post<Post>(`/posts/${id}/publish`)
  },

  archive(id: string) {
    return client.post<Post>(`/posts/${id}/archive`)
  },

  delete(id: string) {
    return client.delete(`/posts/${id}`)
  },

  uploadImage(postId: string, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return client.post<ImageUploadResult>(`/posts/${postId}/images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  getImageDownloadUrl(postId: string, imageId: string) {
    return client.get<{ url: string }>(`/posts/${postId}/images/${imageId}/download`)
  },

  deleteImage(postId: string, imageId: string) {
    return client.delete(`/posts/${postId}/images/${imageId}`)
  },
}
