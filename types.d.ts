import React, { ReactNode } from 'react';

// Fix for React element props
declare module 'react' {
  interface ReactElement {
    props: {
      children?: ReactNode;
      [key: string]: any;
    };
  }
}

// Fix for JSX.IntrinsicElements
declare global {
  namespace JSX {
    interface IntrinsicElements {
      [elemName: string]: any;
    }
  }
}

// SyntaxScope specific types
export type SyntaxItem = {
  id: string;
  command: string;
  description: string;
  category: string;
  tags: string[];
};
