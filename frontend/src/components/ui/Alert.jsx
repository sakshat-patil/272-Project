import React from 'react';
import { AlertCircle, CheckCircle2, Info, XCircle } from 'lucide-react';
import { cn } from '../../utils/cn';

const Alert = ({ className, variant = 'default', children, ...props }) => {
  const variants = {
    default: 'bg-background text-foreground border-border',
    destructive: 'bg-destructive/10 text-destructive border-destructive/50',
    success: 'bg-green-50 text-green-800 border-green-300',
    warning: 'bg-yellow-50 text-yellow-800 border-yellow-300',
    info: 'bg-blue-50 text-blue-800 border-blue-300',
  };

  const icons = {
    default: Info,
    destructive: XCircle,
    success: CheckCircle2,
    warning: AlertCircle,
    info: Info,
  };

  const Icon = icons[variant];

  return (
    <div
      role="alert"
      className={cn(
        'relative w-full rounded-lg border p-4',
        variants[variant],
        className
      )}
      {...props}
    >
      <div className="flex items-start gap-3">
        <Icon className="h-5 w-5 flex-shrink-0 mt-0.5" />
        <div className="flex-1">{children}</div>
      </div>
    </div>
  );
};

export const AlertTitle = ({ className, ...props }) => (
  <h5
    className={cn('mb-1 font-medium leading-none tracking-tight', className)}
    {...props}
  />
);

export const AlertDescription = ({ className, ...props }) => (
  <div
    className={cn('text-sm [&_p]:leading-relaxed', className)}
    {...props}
  />
);

export default Alert;