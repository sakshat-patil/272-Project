import { vi } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios')

export const mockAxios = {
  get: vi.fn(() => Promise.resolve({ data: {} })),
  post: vi.fn(() => Promise.resolve({ data: {} })),
  put: vi.fn(() => Promise.resolve({ data: {} })),
  delete: vi.fn(() => Promise.resolve({ data: {} })),
  create: vi.fn(function () {
    return this
  }),
  defaults: {
    baseURL: 'http://localhost:8000',
  },
  interceptors: {
    request: {
      use: vi.fn(),
      eject: vi.fn(),
    },
    response: {
      use: vi.fn(),
      eject: vi.fn(),
    },
  },
}

// Apply mock to axios
Object.assign(axios, mockAxios)

export default mockAxios
