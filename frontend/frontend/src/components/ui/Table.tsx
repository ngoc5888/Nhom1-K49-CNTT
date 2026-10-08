import * as React from 'react'
import { cn } from '../../lib/utils'

interface TableProps {
  headers: string[]
  children: React.ReactNode
  className?: string
}

export function Table({ headers, children, className }: TableProps) {
  return (
    <div className={cn('overflow-x-auto', className)}>
      <table className="w-full text-sm">
        <thead>
          <tr>
            {headers.map((h) => (
              <th key={h} className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider bg-slate-50 border-b border-slate-100">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-50">{children}</tbody>
      </table>
    </div>
  )
}

interface TdProps extends React.TdHTMLAttributes<HTMLTableCellElement> {}

export function Td({ className, ...props }: TdProps) {
  return (
    <td className={cn('px-4 py-3 text-sm text-slate-700 align-middle', className)} {...props} />
  )
}

interface TrProps extends React.HTMLAttributes<HTMLTableRowElement> {}

export function Tr({ className, ...props }: TrProps) {
  return (
    <tr
      className={cn('hover:bg-slate-50/50 transition-colors duration-150', className)}
      {...props}
    />
  )
}
