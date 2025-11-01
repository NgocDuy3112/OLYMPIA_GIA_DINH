import { useState, useCallback } from 'react';



interface Props {
  title: string;
  description: string;
  status: 'success' | 'error' | 'warning' | 'info';
}



interface PropsWithDuration extends Props {
  duration?: number;
}

export const useSimpleToast = () => {
  const [toastState, setToastState] = useState<Props | null>(null);

  const showToast = useCallback(
    ({ title, description, status, duration = 3000 }: PropsWithDuration) => {
      setToastState({ title, description, status });

      if (duration > 0) {
        const timer = setTimeout(() => setToastState(null), duration);
        return () => clearTimeout(timer);
      }
    },
    []
  );

  const hideToast = useCallback(() => setToastState(null), []);

  return { toastState, showToast, hideToast };
};