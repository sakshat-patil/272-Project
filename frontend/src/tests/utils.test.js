import { describe, it, expect } from 'vitest'
import { formatDate, formatNumber, formatCurrency } from '../utils/formatters'
import { getRiskLevelColor, getRiskScoreColor, formatRiskScore } from '../utils/riskUtils'

describe('Formatters', () => {
  describe('formatDate', () => {
    it('should format date correctly', () => {
      const date = new Date('2024-01-15T10:30:00Z')
      const formatted = formatDate(date)
      expect(formatted).toMatch(/Jan|January/)
      expect(formatted).toMatch(/15/)
      expect(formatted).toMatch(/2024/)
    })

    it('should handle string dates', () => {
      const formatted = formatDate('2024-01-15T10:30:00Z')
      expect(formatted).toBeDefined()
      expect(typeof formatted).toBe('string')
    })
  })

  describe('formatNumber', () => {
    it('should format numbers with commas', () => {
      expect(formatNumber(1000)).toBe('1,000')
      expect(formatNumber(1000000)).toBe('1,000,000')
    })

    it('should handle decimals', () => {
      expect(formatNumber(1234.56)).toMatch(/1,234/)
    })
  })

  describe('formatCurrency', () => {
    it('should format currency with dollar sign', () => {
      const formatted = formatCurrency(1234.56)
      expect(formatted).toMatch(/\$/)
      expect(formatted).toMatch(/1,235/) // Rounds to nearest dollar
    })

    it('should handle large numbers', () => {
      const formatted = formatCurrency(1000000)
      expect(formatted).toMatch(/\$/)
      expect(formatted).toMatch(/1,000,000/)
    })
  })
})

describe('Risk Utils', () => {
  describe('getRiskLevelColor', () => {
    it('should return correct colors for risk levels', () => {
      expect(getRiskLevelColor('LOW')).toContain('blue')
      expect(getRiskLevelColor('MEDIUM')).toContain('yellow')
      expect(getRiskLevelColor('HIGH')).toContain('orange')
      expect(getRiskLevelColor('CRITICAL')).toContain('red')
    })

    it('should have default for unknown levels', () => {
      expect(getRiskLevelColor('UNKNOWN')).toBeDefined()
    })
  })

  describe('getRiskScoreColor', () => {
    it('should return correct colors for risk scores', () => {
      expect(getRiskScoreColor(10)).toContain('green')
      expect(getRiskScoreColor(30)).toContain('blue')
      expect(getRiskScoreColor(50)).toContain('yellow')
      expect(getRiskScoreColor(70)).toContain('orange')
      expect(getRiskScoreColor(90)).toContain('red')
    })
  })

  describe('formatRiskScore', () => {
    it('should format risk scores correctly', () => {
      expect(formatRiskScore(45.67)).toBe(45.7)
      expect(formatRiskScore(89.12)).toBe(89.1)
    })
  })
})
