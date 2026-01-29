'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function TasksRedirectPage() {
  const router = useRouter();

  useEffect(() => {
    router.push('/dashboard/tasks');
  }, [router]);

  return null;
}