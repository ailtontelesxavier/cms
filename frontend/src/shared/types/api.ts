export interface PaginatedResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface ApiErrorDetail {
  detail: string
  code?: string
  field?: string
}

export interface ApiValidationError {
  detail: ApiErrorDetail[]
}
