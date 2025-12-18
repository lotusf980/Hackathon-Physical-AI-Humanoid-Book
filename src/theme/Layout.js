import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import BookChatbot from '@site/src/components/BookChatbot';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <BookChatbot />
    </>
  );
}