import * as React from 'react'
import { cn } from '../../lib/utils'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}
interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}
interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {}
interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn('bg-white rounded-xl border border-slate-100 shadow-sm', className)}
      {...props}
    />
  )
}

export function CardHeader({ className, ...props }: CardHeaderProps) {
  return <div className={cn('px-5 py-4 border-b border-slate-100', className)} {...props} />
}

export function CardTitle({ className, ...props }: CardTitleProps) {
  return (
    <h3 className={cn('text-base font-semibold text-slate-800', className)} {...props} />
  )
}

export function CardContent({ className, ...props }: CardContentProps) {
  return <div className={cn('p-5', className)} {...props} />
}
