import { useState, useEffect } from 'react';

// BAC National exam date — June 4, 2026 at 08:00 local time
const BAC_DATE = new Date('2026-06-04T08:00:00');

export function useBacCountdown() {
  const [timeLeft, setTimeLeft] = useState(calcTimeLeft());

  function calcTimeLeft() {
    const diff = BAC_DATE.getTime() - Date.now();
    if (diff <= 0) return { days: 0, hours: 0, minutes: 0, seconds: 0, total: 0 };
    return {
      total: diff,
      days: Math.floor(diff / (1000 * 60 * 60 * 24)),
      hours: Math.floor((diff / (1000 * 60 * 60)) % 24),
      minutes: Math.floor((diff / (1000 * 60)) % 60),
      seconds: Math.floor((diff / 1000) % 60),
    };
  }

  useEffect(() => {
    const t = setInterval(() => setTimeLeft(calcTimeLeft()), 1000);
    return () => clearInterval(t);
  }, []);

  return timeLeft;
}

interface BacCountdownProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export default function BacCountdown({ size = 'md', className = '' }: BacCountdownProps) {
  const { days, hours, minutes, seconds, total } = useBacCountdown();

  if (total <= 0) {
    return (
      <div className={`text-center text-red-400 font-bold ${className}`}>
        🎓 Bonne chance pour le BAC !
      </div>
    );
  }

  const isUrgent = days <= 7;

  const boxClass =
    size === 'lg'
      ? 'w-16 sm:w-20 bg-white/[.06] border border-white/10 rounded-xl p-2 sm:p-3'
      : size === 'sm'
      ? 'w-10 bg-white/[.06] border border-white/10 rounded-lg p-1.5'
      : 'w-14 bg-white/[.06] border border-white/10 rounded-xl p-2';

  const numClass =
    size === 'lg'
      ? `text-2xl sm:text-3xl font-black tabular-nums ${isUrgent ? 'text-red-400' : 'text-white'}`
      : size === 'sm'
      ? `text-base font-black tabular-nums ${isUrgent ? 'text-red-400' : 'text-white'}`
      : `text-xl font-black tabular-nums ${isUrgent ? 'text-red-400' : 'text-white'}`;

  const labelClass =
    size === 'lg'
      ? 'text-[10px] text-white/40 mt-0.5'
      : size === 'sm'
      ? 'text-[9px] text-white/40 mt-0.5'
      : 'text-[9px] text-white/40 mt-0.5';

  const pad = (n: number) => String(n).padStart(2, '0');

  return (
    <div className={`flex items-center justify-center gap-1.5 sm:gap-2 ${className}`}>
      {[
        { val: days, label: 'Jours' },
        { val: hours, label: 'Heures' },
        { val: minutes, label: 'Min' },
        { val: seconds, label: 'Sec' },
      ].map(({ val, label }, i) => (
        <div key={label}>
          <div className={`${boxClass} text-center`}>
            <div className={numClass}>{i === 0 ? val : pad(val)}</div>
            <div className={labelClass}>{label}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
