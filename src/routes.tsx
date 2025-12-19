import Prompti from './pages/Prompti';
import type { ReactNode } from 'react';

interface RouteConfig {
  name: string;
  path: string;
  element: ReactNode;
  visible?: boolean;
}

const routes: RouteConfig[] = [
  {
    name: 'Prompti',
    path: '/',
    element: <Prompti />
  }
];

export default routes;
